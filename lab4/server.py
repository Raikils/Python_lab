from notebook import Notebook
import Pyro4

if __name__ == '__main__':
	daemon = Pyro4.Daemon()
	uri = daemon.register(Notebook)
	ns = Pyro4.locateNS()
	ns.register('notebook', uri)
	daemon.requestLoop()