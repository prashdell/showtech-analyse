#!/bin/bash

# Simplified Comprehensive Showtech Archive Scrubbing Script
# Processes all showtech archives with robust directory handling

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="${SCRIPT_DIR}/archive_scrubbing_workspace"
LOG_FILE="${SCRIPT_DIR}/archive_scrubbing_workspace/scrubbing_log_$(date +%Y%m%d_%H%M%S).txt"
TEMP_DIR="${WORKSPACE_DIR}/temp_scrubbing"

# Target directories to scrub
TARGET_DIRS=("debugsh" "dump" "etc" "proc" "sai" "warmboot")

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Initialize workspace
init_workspace() {
    log "Initializing workspace..."
    mkdir -p "$TEMP_DIR"
    mkdir -p "${WORKSPACE_DIR}/scrubbed_archives"
    log "Workspace initialized successfully"
}

# IP address scrubbing
scrub_ips() {
    local file="$1"
    sed -i.tmp -r 's/\b([0-9]{1,3}\.){3}[0-9]{1,3}\b/XXX.XXX.XXX.XXX/g' "$file"
    sed -i.tmp -r 's/\b([0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b/XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX/g' "$file"
    rm -f "${file}.tmp"
}

# MAC address scrubbing
scrub_macs() {
    local file="$1"
    sed -i.tmp -r 's/\b([0-9a-fA-F]{2}[:\-]){5}[0-9a-fA-F]{2}\b/XX:XX:XX:XX:XX:XX/g' "$file"
    sed -i.tmp -r 's/\b([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}\b/XXXX.XXXX.XXXX/g' "$file"
    rm -f "${file}.tmp"
}

# Hostname scrubbing
scrub_hostnames() {
    local file="$1"
    sed -i.tmp -r 's/\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}\b/SCRUBBED.HOSTNAME.COM/g' "$file"
    rm -f "${file}.tmp"
}

# Password and key scrubbing
scrub_passwords_keys() {
    local file="$1"
    sed -i.tmp -r 's/password[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/password=SCRUBBED_PASSWORD/gi' "$file"
    sed -i.tmp -r 's/secret[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/secret=SCRUBBED_SECRET/gi' "$file"
    sed -i.tmp -r 's/-----BEGIN [A-Z]+ KEY-----/-----BEGIN SCRUBBED KEY-----/g' "$file"
    sed -i.tmp -r 's/-----END [A-Z]+ KEY-----/-----END SCRUBBED KEY-----/g' "$file"
    rm -f "${file}.tmp"
}

# Platform identifier scrubbing
scrub_platform_identifiers() {
    local file="$1"
    sed -i.tmp -r 's/serial[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/serial=SCRUBBED_SERIAL/gi' "$file"
    sed -i.tmp -r 's/asic[_-]?id[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/asic_id=SCRUBBED_ASIC_ID/gi' "$file"
    rm -f "${file}.tmp"
}

# Comprehensive file scrubbing
scrub_file() {
    local file="$1"
    
    if [[ ! -f "$file" ]] || [[ ! -s "$file" ]]; then
        return
    fi
    
    log "Scrubbing file: $(basename "$file")"
    
    # Apply all scrubbing functions
    scrub_ips "$file"
    scrub_macs "$file"
    scrub_hostnames "$file"
    scrub_passwords_keys "$file"
    scrub_platform_identifiers "$file"
}

# Process directory
process_directory() {
    local source_dir="$1"
    local target_dir="$2"
    
    if [[ ! -d "$source_dir" ]]; then
        log "Directory not found: $source_dir"
        return
    fi
    
    log "Processing directory: $source_dir"
    mkdir -p "$target_dir"
    
    # Process all files recursively
    while IFS= read -r -d '' file; do
        local rel_path="${file#$source_dir/}"
        local target_file="$target_dir/$rel_path"
        local target_dir_path="$(dirname "$target_file")"
        
        mkdir -p "$target_dir_path"
        cp "$file" "$target_file"
        scrub_file "$target_file"
        
    done < <(find "$source_dir" -type f -print0)
}

# Process single archive
process_archive() {
    local archive_path="$1"
    local archive_name="$(basename "$archive_path")"
    local scrubbed_name="${archive_name%.*}_scrubbed.tar.gz"
    
    log "=== Processing archive: $archive_name ==="
    
    # Create extraction directory
    local extract_dir="$TEMP_DIR/${archive_name%.*}"
    mkdir -p "$extract_dir"
    
    # Extract archive
    log "Extracting archive..."
    if [[ "$archive_path" == *.tar.gz ]] || [[ "$archive_path" == *.tgz ]]; then
        tar -xzf "$archive_path" -C "$extract_dir" 2>/dev/null || {
            log "Failed to extract: $archive_path"
            rm -rf "$extract_dir"
            return 1
        }
    elif [[ "$archive_path" == *.tar ]]; then
        tar -xf "$archive_path" -C "$extract_dir" 2>/dev/null || {
            log "Failed to extract: $archive_path"
            rm -rf "$extract_dir"
            return 1
        }
    elif [[ "$archive_path" == *.zip ]]; then
        unzip -q "$archive_path" -d "$extract_dir" 2>/dev/null || {
            log "Failed to extract: $archive_path"
            rm -rf "$extract_dir"
            return 1
        }
    else
        log "Unsupported format: $archive_path"
        rm -rf "$extract_dir"
        return 1
    fi
    
    # Find the main dump directory
    local main_dump_dir=""
    local possible_dirs=("sonic_dump_*" "dump" "showtech" "*dump*")
    
    for pattern in "${possible_dirs[@]}"; do
        main_dump_dir=$(find "$extract_dir" -maxdepth 2 -type d -name "$pattern" | head -1)
        if [[ -n "$main_dump_dir" ]]; then
            break
        fi
    done
    
    # If no specific dump directory found, use the extraction root
    if [[ -z "$main_dump_dir" ]]; then
        main_dump_dir="$extract_dir"
        log "Using extraction root as main directory"
    else
        log "Found main dump directory: $main_dump_dir"
    fi
    
    # Create scrubbed directory
    local scrubbed_base_dir="${WORKSPACE_DIR}/scrubbed_archives/${archive_name%.*}_scrubbed"
    mkdir -p "$scrubbed_base_dir"
    
    # Process target directories
    local processed_targets=0
    for target_dir in "${TARGET_DIRS[@]}"; do
        local source_path="$main_dump_dir/$target_dir"
        local target_path="$scrubbed_base_dir/$target_dir"
        
        if [[ -d "$source_path" ]]; then
            process_directory "$source_path" "$target_path"
            ((processed_targets++))
            log "Processed target directory: $target_dir"
        else
            log "Target directory not found: $target_dir"
        fi
    done
    
    # Copy other files (safe files)
    log "Copying safe files..."
    while IFS= read -r -d '' file; do
        local rel_path="${file#$main_dump_dir/}"
        local target_file="$scrubbed_base_dir/$rel_path"
        local target_dir_path="$(dirname "$target_file")"
        
        # Skip processed target directories
        local should_skip=false
        for target_dir in "${TARGET_DIRS[@]}"; do
            if [[ "$rel_path" == "$target_dir"* ]]; then
                should_skip=true
                break
            fi
        done
        
        if [[ "$should_skip" == false ]]; then
            mkdir -p "$target_dir_path"
            cp "$file" "$target_file"
        fi
        
    done < <(find "$main_dump_dir" -type f -print0 2>/dev/null || true)
    
    # Create scrubbed archive
    if [[ -d "$scrubbed_base_dir" ]] && [[ "$(ls -A "$scrubbed_base_dir")" ]]; then
        log "Creating scrubbed archive: $scrubbed_name"
        cd "$scrubbed_base_dir"
        tar -czf "${WORKSPACE_DIR}/scrubbed_archives/$scrubbed_name" * 2>/dev/null || true
        cd "$SCRIPT_DIR"
        log "Created scrubbed archive: $scrubbed_name"
    else
        log "No files to archive for: $archive_name"
    fi
    
    # Clean up
    rm -rf "$extract_dir"
    rm -rf "$scrubbed_base_dir"
    
    log "=== Completed archive: $archive_name (processed $processed_targets target directories) ==="
    return 0
}

# Find and process all archives
process_all_archives() {
    log "Starting comprehensive archive processing..."
    
    # Find all archives - focus on sonic dumps and showtech archives
    local archives=()
    while IFS= read -r archive; do
        archives+=("$archive")
    done < <(find "$SCRIPT_DIR" -type f \( -name "*.tar.gz" -o -name "*.zip" -o -name "*.tar" \) | grep -E "(sonic_dump|showtech)" | sort)
    
    if [[ ${#archives[@]} -eq 0 ]]; then
        log "No archives found"
        return
    fi
    
    log "Found ${#archives[@]} archives to process"
    
    local processed=0
    local failed=0
    
    for archive in "${archives[@]}"; do
        log "Processing archive $((processed + failed + 1))/${#archives[@]}"
        
        if process_archive "$archive"; then
            ((processed++))
        else
            ((failed++))
        fi
        
        # Clean temp files
        rm -rf "$TEMP_DIR"/*
    done
    
    log "=== Processing Summary ==="
    log "Total archives: ${#archives[@]}"
    log "Successfully processed: $processed"
    log "Failed: $failed"
    log "Scrubbed archives available in: ${WORKSPACE_DIR}/scrubbed_archives/"
}

# Cleanup
cleanup() {
    log "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
    log "Cleanup completed"
}

# Main execution
main() {
    log "=== Comprehensive Showtech Archive Scrubbing Started ==="
    
    init_workspace
    process_all_archives
    cleanup
    
    log "=== Comprehensive Showtech Archive Scrubbing Completed ==="
}

trap cleanup EXIT
main "$@"