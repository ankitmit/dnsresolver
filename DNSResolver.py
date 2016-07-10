import dns.query
import dns.resolver
import dns.message
from dns.exception import DNSException
import os.path
import re
import sys
import UtilFunctions

class DNSResolver:	
	def __init__(self, ns = None):
		self.resolver = dns.resolver
		self.resolver.timeout = 1
		self.resolver.lifetime = 1
		if ns != None:
			self.resolver.override_system_resolver(ns)
	
	def get_ns(self):
		return self.resolver._resolver
	
	def update_ns(self, updated_ns):
		self.resolver.override_system_resolver(updated_ns)
	
	def get_ns_iterative(self, domain):
		partial_domain = ""
		tokens = domain.split('.')
		for token in reversed(tokens):
			partial_domain = str(token) + partial_domain
			ns = self.get_ns_list_recursive(partial_domain)
			if ns != -1:
				self.update_ns(ns)
				partial_domain = "." + partial_domain
			else:
				break
		
		if ns != -1:
			UtilFunctions.UtilFunctions().log2Screen("Querrying the nameserver %s for address of %s" %(ns, domain))
			try:
				myAnswers =  self.resolver.query(domain, "A")
				if len(myAnswers) > 0:
					ns = myAnswers[0]
			except:
				ns = -1
		return ns

	def get_ns_list_recursive(self, domain):
		resolver = self.resolver
		ns = self.get_ns()

		UtilFunctions.UtilFunctions().log2Screen('Querrying the server %s to resolve the domain %s' % (ns, domain))
		query = dns.message.make_query(domain, dns.rdatatype.NS)
		response = dns.query.udp(query, ns)
		rcode = response.rcode()
		if rcode != dns.rcode.NOERROR:
		    if rcode == dns.rcode.NXDOMAIN:
		        raise Exception('%s does not exist.' % (sub))
		    else:
		        return -1
		if len(response.authority) > 0:
		    rrsets = response.authority
		elif len(response.additional) > 0:
		    rrsets = [response.additional]
		else:
		    rrsets = response.answer

		# Handle all RRsets, not just the first one
		for rrset in rrsets:
		    for rr in rrset:
		        if rr.rdtype == dns.rdatatype.SOA:
		            pass
		        elif rr.rdtype == dns.rdatatype.A:
		            ns = rr.items[0].address
		        elif rr.rdtype == dns.rdatatype.NS:
		            authority = rr.target
		            ns = resolver.query(authority).rrset[0].to_text()
		            result = rrset
		return ns
	def get_ip_address(self, domain):
		myAnswers = self.resolver.query(domain, 'A')
		return myAnswers[0]
