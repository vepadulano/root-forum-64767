# Creates dictionary for ROOT::VecOps::RVec<std::vector<std::vector<float>>
# The .rootmap file will be automatically loaded during the Python session
# The libRVecVecVecDict.so library will be automatically searched for 
# If found, the Python session will succesfully load the dictionary
# Then calls to gInterpreter.GenerateDictionary will not be needed
rootcling -f RVecVecVecDict.cxx -s libRVecVecVecDict.so -rml libRVecVecVecDict.so -rmf libRVecVecVecDict.rootmap -c RVecVecVec.hxx RVecVecVecLinkDef.hxx

# Create the expected libRVecVecVecDict.so shared library
g++ $(root-config --cflags --libs) -fPIC RVecVecVecDict.cxx -shared -o libRVecVecVecDict.so
