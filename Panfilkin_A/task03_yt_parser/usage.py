import youtube_parser


def main():
    youtube_parser.main(['', 'comments_example.txt'])
    youtube_parser.main(['', 'comments_example.txt', 'statistics.txt'])


if __name__ == "__main__":
    main()
