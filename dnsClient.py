from dnslib import *
import dns.resolver
import binascii
import socket
import sys


def hexPretty(hexBytes):
	hexStr = binascii.hexlify(hexBytes)
	prettyStr = ""
	for i in range(1, len(hexStr)):
		prettyStr += hexStr[i]
		if i % 2 == 0:
			prettyStr += ' '
		if i % 8 == 0:
			prettyStr += '\n'
	return prettyStr


def main(argv):
	try:
		dns_server = dns.resolver.Resolver().nameservers[0]

		print(argv)

		if len(argv) < 1:
			argv = ['www.google.com']

		v_return = []

		for hostName in argv:
			print('\n\n\tDNS Lookup for : ' + hostName + '\n')

			question = DNSRecord.question(hostName, "A")
			request = question.send(dest=dns_server, port=53, tcp=False)
			response = DNSRecord.parse(request)

			print('\tquestion header : ')
			print(str(question.header) + '\n')
			print('\tresponse header : ')
			print(str(response.header) + '\n')
			print('\n\t:questions')
			print(str(response.questions) + '\n')
			print('\n\t:answers')
			print(str(response.rr) + '\n')

			cnt = 0
			for r in response.rr:
				cnt += 1
				print('answer[' + str(cnt) + ']' + '\t: ' + str(r))

			if len(argv) == 1:
				print('\n\t\t:question bytes\n' + hexPretty(question.pack()) + '\n')
				print('\t\t:answer bytes\n' + hexPretty(request) + '\n')

			v_return.append(str(response.rr[0].rdata) if response and response.rr and response.rr[0] and response.rr[0].rdata else '')
			# v_return.append(socket.gethostbyname(hostName))
	
	except:
		v_return = ['']

	finally:
		return v_return


if __name__ == "__main__":
	main(sys.argv[1:])

"""
	https://www.wikiwand.com/en/List_of_DNS_record_types#/Resource_records
"""