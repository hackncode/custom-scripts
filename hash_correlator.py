# Usage
# python hash_correlator.py -n /path/to/ntds.txt -c /path/to/cracked.txt -o /path/to/output.txt


import argparse
import os

# Function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Correlate cracked hashes with user accounts from an NTDS dump.")
    parser.add_argument("-n", "--ntds", required=True, help="Path to the NTDS file containing user accounts and hashes.")
    parser.add_argument("-c", "--cracked", default="", help="Path to the file containing cracked hashes. Defaults to Hashcat's potfile if not specified.")
    parser.add_argument("-o", "--output", help="Output file path to write the results. Defaults to <ntds_filename>_passwords.txt.")
    return parser.parse_args()

# Function to process files and extract passwords
def process_files(ntds_file, cracked_file, output_file):
    # Use Hashcat's potfile as default if no cracked file path is provided
    if not cracked_file:
        cracked_file = os.path.expanduser("~/.local/share/hashcat/hashcat.potfile")
    
    # Set default output file name if not specified
    if not output_file:
        output_file = f"{ntds_file}_passwords.txt"
    
    try:
        with open(cracked_file, 'r') as cracked:
            with open(output_file, 'a') as output:
                for line in cracked:
                    hash, password = line.strip().split(':', 1)
                    if len(password) > 0:
                        with open(ntds_file, 'r') as ntds:
                            for line2 in ntds:
                                user, ntds_hash = line2.strip().split(':', 1)
                                if hash == ntds_hash:
                                    print(f"{user}:{password}")
                                    output.write(f"{user}:{password}\n")
    except FileNotFoundError as e:
        print(f"Error: {e.strerror} - {e.filename}")
        exit(1)
    
    print(f"All done. Results written to {output_file}.")

# Main function
if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args()

    # Process the files with provided arguments
    process_files(args.ntds, args.cracked, args.output)

