import os, io, time, math, asyncio, subprocess, logging, shutil, shlex, tempfile

#
# id         server      port   user   password   extraopt    sessions
# ===  ================= ===== ====== ========== =========== ==========
#  1    192.168.100.100   623   root     root    -I lanplus      2
#  2    192.168.100.101   623   root     root    -I lanplus      3
# 
#   id for server         task    freq   id as offset (omitted)   next run
# ==================== ========= ====== ======================== ===============
#  1 (192.168.100.100)  sdrlist     5            1                1523500000000
#
# if (currenttime - offset) % freq == 0, perform task

class Monitor():
    ID = 0
    COMMAND = 1
    INTERVAL = 2
    NEXTRUN = 3

    HOST_IP = 1
    HOST_PORT = 2
    HOST_USER = 3
    HOST_PASS = 4
    HOST_EXTRA = 5
    HOST_SESSION = 6

    SERVERID = 'serverid'
    SERVER = 'server'
    STAMP = 'stamp'
    EXEC = 'exec'
    PLANFILE = 'planfile'
    RESULTFILE = 'resultfile'

    # IPMI = 'CHOICE /T 10 /C ync /CS /D y /M "ipmitool.exe' # shutil.which(self.IPMI)
    IPMIPWD = 'IPMI_PASSWORD'

    Ipmi = 'ipmitool.exe'
    # IpmiCommandFormat = "CHOICE /T 10 /C ync /CS /D y /M \"ipmitool.exe -H {erver[1]} -p {server[2]} -U {server[3]} -E {server[5}} exec {planfile}\" >> {resultfile} 2>&1"
    IpmiCommandFormat = " -H {server[1]} -p {server[2]} -U {server[3]} -E {server[5]} exec {planfile} >> {resultfile} 2>&1"
    PlanEndStringFormat = "# Time={stamp}, Server={serverid}"

    PlansDir = os.path.join(tempfile.gettempdir(), 'plans')
    ResultDir = os.path.join(tempfile.gettempdir(), 'results')

    PlanFileFormat = 'plan-{serverid}-{stamp}.txt'
    ResultFileFormat = 'output-{serverid}-{stamp}.txt'

    loop = None
    # store the server table
    servers = []
    # store the task table
    tasks = []
    # store the plan files
    planfiles = {}
    # store the result files
    resultfiles = {}

    # lastRun = 0
    triggerPeriod = 500
    expirePeriod = 600000

    expireTime = 0

    def __init__(self):
        currenttime = self._get_current_time()
        self.expireTime = currenttime
        # self.lastRun = currenttime

        # clean folder before proceed
        self._try_refresh_dir(self.PlansDir)
        self._try_refresh_dir(self.ResultDir)

        self.Ipmi = shutil.which(self.Ipmi)
        if self.Ipmi == '':
            logging.error('IPMI Tool is not found.')
            raise Exception('IPMI Tool is not found.')

        self.IpmiCommandFormat = self.Ipmi + self.IpmiCommandFormat

    def _convert_name(self, command):
        return str(command).replace(' ', '_')

    def _create_empty_session_slot(self, serverid, sessions):
        self.planfiles[serverid] = [''] * sessions
        self.resultfiles[serverid] = [''] * sessions

    def _get_current_time(self):
        return math.floor(time.time() * 1000 / self.triggerPeriod) * self.triggerPeriod

    def _get_plan_file(self, obj):
        # return os.path.join(self.PlansDir, self.PlanPrefix + str(obj[self.STAMP]) + str(obj[self.SERVERID]) + self.PlanPostfix)
        return os.path.join(self.PlansDir, self.PlanFileFormat.format(**obj))

    def _get_result_file(self, obj):
        # return os.path.join(self.ResultDir, self.ResultPrefix + str(obj[self.STAMP]) + str(obj[self.SERVERID]) + self.ResultPostfix)
        return os.path.join(self.ResultDir, self.ResultFileFormat.format(**obj))

    def _get_server_from_id(self, serverid):
        servers = [serv for serv in self.servers if serv[0] == serverid]

        if len(servers) != 1:
            logging.error('server id={} has {} instance(s).'.format(serverid, len(servers)))
            return []

        return servers[0]

    def _get_time_string(self, milsec):
        return time.strftime('%Y%m%d%H%M%S', time.localtime(milsec / 1000.0))

    def _has_empty_session(self, serverid):
        server = self._get_server_from_id(serverid)
        sessions = server[self.HOST_SESSION]

        if serverid not in self.resultfiles: # new if not exist
            self._create_empty_session_slot(serverid, sessions)
            return True, 0
        elif len(self.resultfiles[serverid]) != sessions: # resized
            if self._is_all_empty(self.resultfiles[serverid]):
                self._create_empty_session_slot(serverid, sessions)
                return True, 0
            else:
                for sessionid in range(sessions):
                    if self.resultfiles[serverid][sessionid] != '':
                        return False, sessionid

                logging.fatal('Invalid session status.')

        for sessionid in range(sessions):
            if self.resultfiles[serverid][sessionid] == '':
                return True, sessionid

        return False, 0

    def _is_all_empty(self, sessions):
        for session in sessions:
            if session != '':
                return False

        return True

    def _try_collect_session_result(self, serverid, sessionid):
        # this method ensure the output is created and renamable, once it complete, clean the previous plan, previous ipmitool step is completed
        if os.path.isfile(self.resultfiles[serverid][sessionid]):
            try:
                os.rename(self.resultfiles[serverid][sessionid], self.resultfiles[serverid][sessionid] + ".1")
            except:
                pass # failed by design
                return False


        lines = []
        fhplan = open(self.planfiles[serverid][sessionid], 'r')
        lines.extend(fhplan.readlines())
        fhplan.close()
        # fhcomplete.writelines(lines)

        fhresult = open(self.resultfiles[serverid][sessionid] + ".1", 'r')
        lines.extend(fhresult.readlines())
        fhresult.close()

        os.remove(self.planfiles[serverid][sessionid])
        os.remove(self.resultfiles[serverid][sessionid] + ".1")

        fhcomplete = open(self.resultfiles[serverid][sessionid] + ".2", 'a')
        fhcomplete.writelines(lines)
        fhcomplete.close()

        self.resultfiles[serverid][sessionid] = ''

        return True

    def _try_refresh_dir(self, path):
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
        except Exception as ex:
            logging.error('Remove Failed: ' + str(ex))

        if not os.path.isdir(path):
            os.makedirs(path)

    ###
    ###
    ###

    def get_servers(self):
        return [
            [1, '192.168.1.100', '623', 'root', 'root', '-I lanplus', 2],
            [2, '192.168.1.101', '623', 'admin', 'admin', '-I lanplus', 10]
        ]

    def get_tasks(self):
        currenttime = self._get_current_time()
        tasks = [
            [1, 'sdr list', 5, currenttime],
            [1, 'mc info', 60, currenttime],
            [2, 'sel list', 1, currenttime],
            [2, 'sdr list', 1, currenttime],
            [2, 'mc info', 10, currenttime]
        ]
        for task in tasks:
            # add offset is to stagger the task for each server
            task[self.NEXTRUN] += (int(task[self.ID]) + task[self.INTERVAL]) * 1000  # milsec

        return tasks

    def add_task(self, obj, task):
        obj[self.EXEC].extend([
            '# driver=' + self._convert_name(task[self.COMMAND]),
            task[self.COMMAND],
            '# 01 84 14 03 00 00 00 00',
            'raw 0x06 0x38 0x8e 0x04'
        ])

    def can_submitable(self, obj, serverid = None):

        if serverid is None:
            return False

        success = False

        try:
            serverid = obj[self.SERVERID]
            obj[self.PLANFILE] = self._get_plan_file(obj)
            obj[self.RESULTFILE] = self._get_result_file(obj)

            found, sessionid = self._has_empty_session(serverid)
            if not found and not self._try_collect_session_result(serverid, sessionid):
                return success # False

            obj[self.EXEC].extend([self.PlanEndStringFormat.format(**obj),])

            fhplan = open(obj[self.PLANFILE], 'w')
            fhplan.write('\n'.join(obj[self.EXEC]) + '\n')
            fhplan.close()

            if serverid not in self.resultfiles:
                self._create_empty_session_slot(serverid, self.servers[serverid][self.HOST_SESSION])

            self.planfiles[serverid][sessionid] = obj[self.PLANFILE]
            self.resultfiles[serverid][sessionid] = obj[self.RESULTFILE]

            success = True

        except Exception as ioex:
            logging.error('File Create Failed: ' + str(ioex))

        return success

    def submit(self, obj):
        try:
            os.environ[self.IPMIPWD] = str(obj[self.SERVER][self.HOST_PASS])
            command = self.IpmiCommandFormat.format(**obj)
            subprocess.Popen(args=shlex.split(command, posix=False), shell=True)

        except Exception as ex:
            logging.error('Submit Failed: ' + str(ex))

    def Dispatcher(self, loop, obj=None):

        if obj is None:
            obj = {}

        loop.call_later(self.triggerPeriod / 1000.0, self.Dispatcher, loop, obj)

        currenttime = self._get_current_time()

        if currenttime > self.expireTime:
            self.servers = self.get_servers()
            self.tasks = self.get_tasks()
            self.expireTime = self.expireTime + self.expirePeriod  # 10 minutes

        serverid = None
        sessionid = None

        for task in self.tasks:
            # skip if task has not expired
            if task[self.NEXTRUN] > currenttime:
                continue

            # server id is changed
            if serverid != task[self.ID]:
                if self.can_submitable(obj, serverid):
                    self.submit(obj)

                serverid = task[self.ID]
                server = self._get_server_from_id(serverid)

                if len(server) != 0:
                    obj[self.SERVERID] = serverid
                    obj[self.SERVER] = server
                    obj[self.STAMP] = self._get_time_string(currenttime)
                    obj[self.EXEC] = [
                        '# 01 84 14 03 00 00 00 00',
                        'raw 0x06 0x38 0x8e 0x04'
                    ]

            self.add_task(obj, task)
            task[self.NEXTRUN] += task[self.INTERVAL] * 1000

        #if serverid is not None:
        #    while not self.can_submitable(obj, serverid):
        #        time.sleep(1)

        if self.can_submitable(obj, serverid):
            self.submit(obj)

        # collect result if finished
        for server in self.servers:
            serverid = server[self.ID]
            if serverid not in self.resultfiles:
                continue

            for sessionid in range(server[self.HOST_SESSION]):
                if self.resultfiles[serverid][sessionid] != '':
                    try:
                        self._try_collect_session_result(serverid, sessionid)
                    except:
                        pass

    def Run(self):
        loop = asyncio.get_event_loop()
        # while True:
        try:
            loop.call_soon(self.Dispatcher, loop)
            loop.run_forever()
            loop.close()
        except Exception as ex:
            logging.error('Thread Failed: ' + str(ex))

if __name__ == '__main__':
    theMonitor = Monitor()
    theMonitor.Run()