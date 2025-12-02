import os

def list_files(startpath):
    # Folders to ignore to keep the output clean
    ignore_dirs = {'.git', '.next', 'node_modules', '__pycache__', '.vscode', '.idea'}
    
    print(f"\nProject Structure for: {os.path.abspath(startpath)}\n")

    for root, dirs, files in os.walk(startpath):
        # Filter out ignored directories from the walk
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        
        # Calculate depth for indentation
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        
        # Print the current folder name
        print(f"{indent}[{os.path.basename(root)}/]")
        
        # Print files in this folder
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f"{subindent}{f}")

if __name__ == "__main__":
    # Runs in the current directory
    list_files('.')