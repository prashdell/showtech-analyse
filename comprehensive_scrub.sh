#!/bin/bash

# Comprehensive Showtech Archive Scrubbing Script
# Processes all specified directories (/debugsh, /core, /etc, /proc, /sai, /warmboot)
# Scrubs sensitive data: IPs, hostnames, MAC addresses, passwords, keys, platform identifiers

set -euo pipefail

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="${SCRIPT_DIR}/archive_scrubbing_workspace"
LOG_FILE="${SCRIPT_DIR}/archive_scrubbing_workspace/scrubbing_log_$(date +%Y%m%d_%H%M%S).txt"
TEMP_DIR="${WORKSPACE_DIR}/temp_scrubbing"

# Target directories to scrub
TARGET_DIRS=("/debugsh" "/dump" "/etc" "/proc" "/sai" "/warmboot")

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Error handling
error_exit() {
    log "ERROR: $1"
    exit 1
}

# Initialize workspace
init_workspace() {
    log "Initializing workspace..."
    mkdir -p "$TEMP_DIR"
    mkdir -p "${WORKSPACE_DIR}/scrubbed_archives"
    
    log "Workspace initialized successfully"
}

# Find all showtech archives
find_archives() {
    log "Finding all showtech archives..."
    
    local archives=()
    
    # Look for archives in multiple locations
    local search_paths=(
        "$WORKSPACE_DIR/downloads"
        "$SCRIPT_DIR/sjobs"
        "$SCRIPT_DIR/data"
        "$SCRIPT_DIR"
    )
    
    for search_path in "${search_paths[@]}"; do
        if [[ -d "$search_path" ]]; then
            while IFS= read -r archive; do
                archives+=("$archive")
            done < <(find "$search_path" -type f \( -name "*.tar.gz" -o -name "*.zip" -o -name "*.tar" \) | grep -E "(sonic|showtech|2025|2026)" | sort)
        fi
    done
    
    log "Found ${#archives[@]} archives to process"
    printf '%s\n' "${archives[@]}"
}

# IP address scrubbing
scrub_ips() {
    local file="$1"
    log "Scrubbing IPs in: $file"
    
    # IPv4 addresses
    sed -i.tmp -r 's/\b([0-9]{1,3}\.){3}[0-9]{1,3}\b/XXX.XXX.XXX.XXX/g' "$file"
    
    # IPv6 addresses (simplified pattern)
    sed -i.tmp -r 's/\b([0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}\b/XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX:XXXX/g' "$file"
    
    rm -f "${file}.tmp"
}

# MAC address scrubbing
scrub_macs() {
    local file="$1"
    log "Scrubbing MAC addresses in: $file"
    
    # MAC addresses in various formats
    sed -i.tmp -r 's/\b([0-9a-fA-F]{2}[:\-]){5}[0-9a-fA-F]{2}\b/XX:XX:XX:XX:XX:XX/g' "$file"
    sed -i.tmp -r 's/\b([0-9a-fA-F]{4}\.){2}[0-9a-fA-F]{4}\b/XXXX.XXXX.XXXX/g' "$file"
    
    rm -f "${file}.tmp"
}

# Hostname scrubbing
scrub_hostnames() {
    local file="$1"
    log "Scrubbing hostnames in: $file"
    
    # Common hostname patterns
    sed -i.tmp -r 's/\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}\b/SCRUBBED.HOSTNAME.COM/g' "$file"
    sed -i.tmp -r 's/\b[a-zA-Z0-9]([a-zA-Z0-9\-]{0,30}[a-zA-Z0-9])?\b/SCRUBBED-HOSTNAME/g' "$file"
    
    rm -f "${file}.tmp"
}

# Password and key scrubbing
scrub_passwords_keys() {
    local file="$1"
    log "Scrubbing passwords and keys in: $file"
    
    # Password patterns
    sed -i.tmp -r 's/password[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/password=SCRUBBED_PASSWORD/gi' "$file"
    sed -i.tmp -r 's/passwd[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/passwd=SCRUBBED_PASSWORD/gi' "$file"
    sed -i.tmp -r 's/secret[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/secret=SCRUBBED_SECRET/gi' "$file"
    
    # Key patterns (private keys, certificates)
    sed -i.tmp -r 's/-----BEGIN [A-Z]+ KEY-----/-----BEGIN SCRUBBED KEY-----/g' "$file"
    sed -i.tmp -r 's/-----END [A-Z]+ KEY-----/-----END SCRUBBED KEY-----/g' "$file"
    sed -i.tmp -r 's/-----BEGIN CERTIFICATE-----/-----BEGIN SCRUBBED CERTIFICATE-----/g' "$file"
    sed -i.tmp -r 's/-----END CERTIFICATE-----/-----END SCRUBBED CERTIFICATE-----/g' "$file"
    
    # API keys and tokens
    sed -i.tmp -r 's/api[_-]?key[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]{10,}["\x27]?/api_key=SCRUBBED_API_KEY/gi' "$file"
    sed -i.tmp -r 's/token[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]{10,}["\x27]?/token=SCRUBBED_TOKEN/gi' "$file"
    
    rm -f "${file}.tmp"
}

# Platform identifier scrubbing
scrub_platform_identifiers() {
    local file="$1"
    log "Scrubbing platform identifiers in: $file"
    
    # Serial numbers
    sed -i.tmp -r 's/serial[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/serial=SCRUBBED_SERIAL/gi' "$file"
    sed -i.tmp -r 's/serial[_-]?number[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/serial_number=SCRUBBED_SERIAL/gi' "$file"
    
    # Platform-specific identifiers
    sed -i.tmp -r 's/asic[_-]?id[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/asic_id=SCRUBBED_ASIC_ID/gi' "$file"
    sed -i.tmp -r 's/chassis[_-]?id[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/chassis_id=SCRUBBED_CHASSIS_ID/gi' "$file"
    sed -i.tmp -r 's/slot[[:space:]]*=[[:space:]]*["\x27]?[^"'\''[:space:]]+["\x27]?/slot=SCRUBBED_SLOT/gi' "$file"
    
    rm -f "${file}.tmp"
}

# Process information scrubbing
scrub_process_info() {
    local file="$1"
    log "Scrubbing process information in: $file"
    
    # PID scrubbing (keep structure but anonymize)
    sed -i.tmp -r 's/\b[0-9]{1,6}\b/PID_SCRUBBED/g' "$file"
    
    # User information
    sed -i.tmp -r 's/[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/USER@SCRUBBED.DOMAIN/g' "$file"
    
    rm -f "${file}.tmp"
}

# Core dump scrubbing
scrub_core_dump() {
    local file="$1"
    log "Scrubbing core dump: $file"
    
    # For binary core dumps, we need to handle them differently
    if file "$file" | grep -q "ELF"; then
        log "Binary core file detected, creating placeholder"
        # Create a placeholder indicating the file was scrubbed
        echo "CORE_DUMP_SCRUBBED: Original binary core file removed for security" > "$file.scrubbed"
        rm -f "$file"
        mv "$file.scrubbed" "$file"
    else
        # For text-based dumps, apply general scrubbing
        scrub_ips "$file"
        scrub_macs "$file"
        scrub_hostnames "$file"
        scrub_passwords_keys "$file"
        scrub_platform_identifiers "$file"
    fi
}

# Comprehensive file scrubbing
scrub_file() {
    local file="$1"
    local file_type="$2"
    
    log "Processing file: $file (type: $file_type)"
    
    # Skip if file doesn't exist or is empty
    if [[ ! -f "$file" ]] || [[ ! -s "$file" ]]; then
        log "Skipping empty or non-existent file: $file"
        return
    fi
    
    # Apply scrubbing based on file type and location
    case "$file_type" in
        "debugsh")
            scrub_ips "$file"
            scrub_macs "$file"
            scrub_hostnames "$file"
            scrub_passwords_keys "$file"
            ;;
        "core")
            scrub_core_dump "$file"
            ;;
        "etc")
            scrub_ips "$file"
            scrub_passwords_keys "$file"
            scrub_hostnames "$file"
            scrub_platform_identifiers "$file"
            ;;
        "proc")
            scrub_ips "$file"
            scrub_process_info "$file"
            scrub_hostnames "$file"
            ;;
        "sai")
            scrub_ips "$file"
            scrub_macs "$file"
            scrub_platform_identifiers "$file"
            ;;
        "warmboot")
            scrub_ips "$file"
            scrub_macs "$file"
            scrub_hostnames "$file"
            scrub_platform_identifiers "$file"
            ;;
        *)
            log "Unknown file type: $file_type, applying general scrubbing"
            scrub_ips "$file"
            scrub_macs "$file"
            scrub_hostnames "$file"
            scrub_passwords_keys "$file"
            ;;
    esac
    
    log "Completed scrubbing: $file"
}

# Process directory
process_directory() {
    local source_dir="$1"
    local target_dir="$2"
    local dir_type="$3"
    
    log "Processing directory: $source_dir -> $target_dir (type: $dir_type)"
    
    if [[ ! -d "$source_dir" ]]; then
        log "Directory not found: $source_dir"
        return
    fi
    
    mkdir -p "$target_dir"
    
    # Process all files in directory recursively
    while IFS= read -r -d '' file; do
        local rel_path="${file#$source_dir/}"
        local target_file="$target_dir/$rel_path"
        local target_dir_path="$(dirname "$target_file")"
        
        # Create target directory if needed
        mkdir -p "$target_dir_path"
        
        # Copy file to target location
        cp "$file" "$target_file"
        
        # Scrub the file
        scrub_file "$target_file" "$dir_type"
        
    done < <(find "$source_dir" -type f -print0)
    
    log "Completed processing directory: $source_dir"
}

# Process single archive
process_archive() {
    local archive_path="$1"
    local archive_name="$(basename "$archive_path")"
    local scrubbed_name="${archive_name%.*}_scrubbed.tar.gz"
    
    log "Processing archive: $archive_name"
    
    # Create extraction directory
    local extract_dir="$TEMP_DIR/${archive_name%.*}"
    mkdir -p "$extract_dir"
    
    # Extract archive
    log "Extracting archive: $archive_path"
    if [[ "$archive_path" == *.tar.gz ]] || [[ "$archive_path" == *.tgz ]]; then
        tar -xzf "$archive_path" -C "$extract_dir"
    elif [[ "$archive_path" == *.tar ]]; then
        tar -xf "$archive_path" -C "$extract_dir"
    elif [[ "$archive_path" == *.zip ]]; then
        unzip -q "$archive_path" -d "$extract_dir"
    else
        log "Unsupported archive format: $archive_path"
        return 1
    fi
    
    # Find the sonic dump directory
    local sonic_dump_dir=$(find "$extract_dir" -maxdepth 2 -type d -name "sonic_dump_*" | head -1)
    if [[ -z "$sonic_dump_dir" ]]; then
        log "Sonic dump directory not found in: $archive_name"
        # Try to find any directory with target subdirectories
        local found_dir=""
        for target_dir in "${TARGET_DIRS[@]}"; do
            local test_dir=$(find "$extract_dir" -name "${target_dir#/}" -type d | head -1)
            if [[ -n "$test_dir" ]]; then
                found_dir="$(dirname "$test_dir")"
                break
            fi
        done
        
        if [[ -z "$found_dir" ]]; then
            log "No suitable directory structure found in: $archive_name"
            return 1
        else
            sonic_dump_dir="$found_dir"
        fi
    fi
    
    log "Found dump directory: $sonic_dump_dir"
    
    # Create scrubbed directory
    local scrubbed_base_dir="${WORKSPACE_DIR}/scrubbed_archives/${archive_name%.*}_scrubbed"
    local scrubbed_sonic_dir="$scrubbed_base_dir/$(basename "$sonic_dump_dir")"
    
    mkdir -p "$scrubbed_sonic_dir"
    
    # Process each target directory
    for target_dir in "${TARGET_DIRS[@]}"; do
        local source_path="$sonic_dump_dir/${target_dir#/}"
        local target_path="$scrubbed_sonic_dir/${target_dir#/}"
        
        # Map directory names to types
        local dir_type="$target_dir"
        if [[ "$target_dir" == "/dump" ]]; then
            dir_type="core"
        else
            dir_type="${target_dir#/}"  # Remove leading slash
        fi
        
        process_directory "$source_path" "$target_path" "$dir_type"
    done
    
    # Copy non-target files (safe files)
    log "Copying safe files..."
    while IFS= read -r -d '' file; do
        local rel_path="${file#$sonic_dump_dir/}"
        local target_file="$scrubbed_sonic_dir/$rel_path"
        local target_dir_path="$(dirname "$target_file")"
        
        # Skip target directories
        local should_skip=false
        for target_dir in "${TARGET_DIRS[@]}"; do
            if [[ "$rel_path" == "${target_dir#/}"* ]]; then
                should_skip=true
                break
            fi
        done
        
        if [[ "$should_skip" == false ]]; then
            mkdir -p "$target_dir_path"
            cp "$file" "$target_file"
        fi
        
    done < <(find "$sonic_dump_dir" -type f -print0)
    
    # Create scrubbed archive
    log "Creating scrubbed archive: $scrubbed_name"
    cd "$scrubbed_base_dir"
    tar -czf "${WORKSPACE_DIR}/scrubbed_archives/$scrubbed_name" *
    cd "$SCRIPT_DIR"
    
    # Clean up extraction directory
    rm -rf "$extract_dir"
    
    log "Completed processing archive: $archive_name"
}

# Main processing function
process_all_archives() {
    log "Starting comprehensive archive scrubbing..."
    
    local archives=()
    while IFS= read -r archive; do
        archives+=("$archive")
    done < <(find_archives)
    
    if [[ ${#archives[@]} -eq 0 ]]; then
        log "No archives found to process"
        return
    fi
    
    log "Processing ${#archives[@]} archives..."
    
    local processed=0
    local failed=0
    
    for archive in "${archives[@]}"; do
        log "=== Processing archive $((processed + failed + 1))/${#archives[@]} ==="
        
        if process_archive "$archive"; then
            ((processed++))
            log "Successfully processed: $(basename "$archive")"
        else
            ((failed++))
            log "Failed to process: $(basename "$archive")"
        fi
        
        # Clean up temporary files
        rm -rf "$TEMP_DIR"/*
        
        log "Progress: $processed processed, $failed failed"
    done
    
    log "=== Processing Complete ==="
    log "Total archives: ${#archives[@]}"
    log "Successfully processed: $processed"
    log "Failed: $failed"
}

# Cleanup function
cleanup() {
    log "Cleaning up temporary files..."
    rm -rf "$TEMP_DIR"
    log "Cleanup completed"
}

# Main execution
main() {
    log "=== Comprehensive Showtech Archive Scrubbing Started ==="
    log "Script: $0"
    log "Workspace: $WORKSPACE_DIR"
    log "Log file: $LOG_FILE"
    
    # Initialize
    init_workspace
    
    # Process all archives
    process_all_archives
    
    # Cleanup
    cleanup
    
    log "=== Comprehensive Showtech Archive Scrubbing Completed ==="
    log "Scrubbed archives are available in: ${WORKSPACE_DIR}/scrubbed_archives/"
    log "Processing log: $LOG_FILE"
}

# Trap for cleanup
trap cleanup EXIT

# Run main function
main "$@"