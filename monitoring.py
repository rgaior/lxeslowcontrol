from argparse import ArgumentParser
import shlex, subprocess

def main():
    print()
    print("--------------------------------------")
    print("LXE MONOITORING SOFT")
    print("--------------------------------------")
    print()

    parser = ArgumentParser("monitoring")
    parser.add_argument("--verbose", help="Shows informations and statistics about the database", action='store_true')
    parser.add_argument("--temp", help="connects to the CTC100 and log the measurements in a file and fill the database", action='store_true')
    parser.add_argument("--hv", help="checks the CAEN log file and fill the data baseShows informations and statistics about the database", action='store_true')
    parser.add_argument("--display", help="open a browser with the influxdb dashboard", action='store_true')
    args = parser.parse_args()
    verbose = args.verbose
    temp = args.temp
    hv = args.hv
    display = args.display
    
    if display:
        print("start display")
        url = 'http://localhost:8086/orgs/0202ae58ef50b477/dashboards/0b80b5cd2e644000?lower=now%28%29%20-%206h'

        command_line = 'x-www-browser ' + url
        command = shlex.split(command_line)
        p = subprocess.Popen(command)        

    if temp:
        import ctc100log
        ctc100log.log()

    if hv:
        import caenlog
        caenlog.log()


if __name__ == "__main__":
    main()
