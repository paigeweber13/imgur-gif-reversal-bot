# -*- coding: utf-8 -*-

# from context import imgur_interface
import context

def main():
    interface = context.ii.ImgurInterface()
    interface.refresh_access_token()

if __name__ == '__main__':
    main()