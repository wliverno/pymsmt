#!/bin/bash
# Script for patching AmberTools environment with code
# Use the --restore flag to undo changes to MCPB.py

if [[ -z "$AMBERHOME" ]]; then
    echo "ERROR: \$AMBERHOME not set, unable to find AmberTools directory"
    exit 1
fi

# Find the Python package directory
PYDIR=$(python3 -c "import site; print(site.getsitepackages()[0])" 2>/dev/null)

if [[ -z "$PYDIR" ]]; then
    echo "ERROR: Unable to determine Python package directory"
    exit 1
fi

echo "Using Python package directory: $PYDIR"

if [[ "$1" == "--restore" ]]; then
    for dir in "$PYDIR"/pymsmt/{mcpb,mol}; do
        for file in "$dir"/*.backup; do
            mv "$file" "${file%.backup}"
        done
    done
    if [[ -f "$PYDIR/pymsmt/lib.py.backup" ]]; then
        mv "$PYDIR/pymsmt/lib.py.backup" "$PYDIR/site-packages/pymsmt/lib.py"
    else
        echo "ERROR: lib.py backup not found! Could not restore..."
    fi
    if [[ -f "$AMBERHOME/bin/MCPB.py.backup" ]]; then
        mv "$AMBERHOME/bin/MCPB.py.backup" "$AMBERHOME/bin/MCPB.py"
    else
        echo "ERROR: MCPB.py backup not found! Could not restore..."
    fi
    echo "MCPB.py files restored."
else
    echo "Adding mmDNA force field information..."
    cp ./mmDNA/mmDNA.mol2 "$AMBERHOME/dat/pymsmt/"
    cp ./mmDNA/leaprc.mmDNA.bsc1 "$AMBERHOME/dat/leap/cmd/"
    cp ./mmDNA/frcmod.parmbsc1_mmDNA "$AMBERHOME/dat/leap/parm/"
    cp ./mmDNA/parmBSC1_mmDNA.lib "$AMBERHOME/dat/leap/lib/"

    echo "Patching python files..."
    cp -b -S .backup ./mcpb/gene* "$PYDIR/pymsmt/mcpb/"
    cp -b -S .backup ./pymsmtmol/mol.py "$PYDIR/pymsmt/mol/"
    cp -b -S .backup ./pymsmtmol/element.py "$PYDIR/pymsmt/mol/"
    cp -b -S .backup ./pymsmtmol/pdbio.py "$PYDIR/pymsmt/mol/"
    cp -b -S .backup ./pymsmtmol/gauio.py "$PYDIR/pymsmt/mol/"
    cp -b -S .backup ./lib.py "$PYDIR/pymsmt/"
    cp -b -S .backup ./tools/MCPB.py "$AMBERHOME/bin/"
    echo "Patch applied to AmberTools environment"
fi

