#!/bin/bash

# Build/compile COBOL programs

echo "Building COBOL programs..."

COBOL_SRC="../../backend/cobol/src"
COBOL_BUILD="../../backend/cobol/build"
COPYBOOKS="../../backend/cobol/copybooks"

# Create build directory if it doesn't exist
mkdir -p "$COBOL_BUILD"

# Compile each COBOL program
for cobol_file in "$COBOL_SRC"/*.{cbl,cob}; do
    if [ -f "$cobol_file" ]; then
        filename=$(basename "$cobol_file")
        program_name="${filename%.*}"
        
        echo "Compiling $filename..."
        
        # Example using GnuCOBOL (cobc)
        # Adjust compiler command based on your COBOL compiler
        cobc -x -o "$COBOL_BUILD/$program_name" -I "$COPYBOOKS" "$cobol_file"
        
        if [ $? -eq 0 ]; then
            echo "✓ Successfully compiled $filename"
        else
            echo "✗ Failed to compile $filename"
            exit 1
        fi
    fi
done

echo "COBOL build complete!"
