import sys, os
sys.path.append(os.environ['QUANT_HOME'] + '/component')
import ServiceClass

ServiceClass.main(sys.argv[1])
#ServiceClass.ProcessManager(host='0.0.0', port=5871).start()