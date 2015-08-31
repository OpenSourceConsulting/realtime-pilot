import sys, os
sys.path.append(os.environ['QUANT_HOME'] + '/lib')
import ServiceClass

ServiceClass.main(sys.argv[1])