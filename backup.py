#!/usr/bin/python

import os
import argparse
import sh
import datetime

argumentParser = argparse.ArgumentParser(
            description = 'Automatically Backup a RAILS-Mongo app from a server to another.'
        )
argumentParser.add_argument(
            '-s', 
            '--server-ip',
            dest = 'serverIp',
            nargs = 1,
            default = '127.0.0.1',
            type = str, 
            help = 'Server IP that must be backuped. Default value is ip of local host.'
        )
argumentParser.add_argument(
            '-f',
            '--bc-folder',
            dest = 'bcFolder',
            nargs = 1,
            required = True,
            type = str,
            help = 'Backup folder on destination server.'
        )
argumentParser.add_argument(
            '-b',
            '--origin-folder',
            dest = 'originFolder',
            nargs = 1,
            required = True, 
            type = str,
            help = 'Folder that you want to backup saves on it.'
        )
argumentParser.add_argument(
            '-u',
            '--username',
            dest = 'username',
            nargs = 1,
            type = str,
            help = 'Username on destionation server that scp connect with it. Default value is root.',
            default = 'root'
        )
argumentParser.add_argument(
            '-t',
            '--time-append',
            dest = 'timeAppend',
            action = 'store_true',
            help = 'Create a folder based on time and save backup on it.'
        )
argumentParser.add_argument(
            '-m',
            '--mongo-path',
            dest = 'mongoPath',
            type = str,
            required = True,
            help = 'Temporary folder for save mongo data.'
        )

args = argumentParser.parse_args()

originAddress = args.originFolder if type(args.originFolder) is str else args.originFolder[0]
if args.timeAppend:
    originAddress += '/' + str(datetime.datetime.now())
    if (not os.path.exists(originAddress)):
        os.makedirs(originAddress)

bcFolder = agrs.bcFolder if type(args.bcFolder) is str else args.bcFolder[0]
serverAddress = ''.join([
                    ':',
                    bcFolder
                ])

sh.scp(
        "-rpq",
        args.username[0] + "@" + args.serverIp[0] + serverAddress,
        originAddress
      )

sh.ssh(
        args.username[0] + "@" + args.serverIp[0],
        'mongodump --out ' + args.mongoPath
      )

sh.scp(
        "-rpq",
        args.username[0] + "@" + args.serverIp[0] + ':' + args.mongoPath,
        originAddress
      )
