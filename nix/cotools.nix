{lib, buildPythonPackage, fetchPypi}:

buildPythonPackage rec {
    pname = "cord-19-tools";
    version = "0.0.7";

    src = fetchPypi {
      inherit pname version;
      sha256 = "aff320bd1e2df2b7a68d5d775a233991bb829ce10035cc085547f43ab3b545d3";
    };
    doCheck = false;
}
