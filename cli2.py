def start():
    parser = argparse.ArgumentParser(description='XfinityFugazi')
    parser.add_argument('-e', '--essid', type=str, help='ESSID of rogue AP', required=True)
    parser.add_argument('-c', '--channel', type=int, help='Channel of rogue AP', required=True)
    args = parser.parse_args()

    rogue_ap = RogueAP(args.essid, args.channel)
    rogue_ap.create_ap()

if __name__ == '__main__':
    start()