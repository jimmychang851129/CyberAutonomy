import sslyze
try:
	server_tester = sslyze.server_connectivity_tester.ServerConnectivityTester(
        hostname='https://nabla-c0d3.github.io/sslyze/documentation/',
        tls_wrapped_protocol=TlsWrappedProtocolEnum.STARTTLS_SMTP
	)
except sslyze.server_connectivity_tester.ServerConnectivityTester as e:
	raise RuntimeError(f'Could not connect to {e.server_info.hostname}: {e.error_message}')
