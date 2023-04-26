import subprocess

class NetworkDebug:
    def __init__(self, target_ip):
        self.target_ip = target_ip

    def ping(self):
        ping_output = subprocess.check_output(['ping', '-c', '4', self.target_ip]).decode('utf-8')
        return ping_output

    def traceroute(self):
        traceroute_output = subprocess.check_output(['traceroute', self.target_ip]).decode('utf-8')
        return traceroute_output

    def mtr(self):
        mtr_output = subprocess.check_output(['mtr', '--report', self.target_ip]).decode('utf-8')
        return mtr_output

    def tcpdump(self):
        tcpdump_output = subprocess.check_output(['tcpdump', '-i', 'eth0', '-n', 'host', self.target_ip]).decode('utf-8')
        return tcpdump_output

    def network_debug(self):
        report = ''
        report += '\nPing output:\n'
        report += self.ping()
        report += '\nTraceroute output:\n'
        report += self.traceroute()
        report += '\nMTR output:\n'
        report += self.mtr()
        report += '\nTCPDump output:\n'
        report += self.tcpdump()

        with open('network_debug_report.txt', 'w') as f:
            f.write(report)

        print('Network debugging report saved to network_debug_report.txt')
