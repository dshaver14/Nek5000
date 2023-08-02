
import sys
from shutil import copyfile
import os
import subprocess

if sys.version_info < (3, 6):
    print("Sorry, requires Python > 3.6")
    sys.exit(1)

from lib.nekTestCase import (
    NekTestCase,
    pn_pn_parallel,
    pn_pn_2_parallel,
    pn_pn_serial,
)

###############################################################################


class Tools(NekTestCase):
    def setUp(self):

        self.build_tools(["all"])

    @pn_pn_parallel
    def test_PnPn_Parallel(self):
        self.assertDelayedFailures()


###############################################################################

class Channel(NekTestCase):
    example_subdir = "RANS_tests/Resolved/Channel"
    case_name = "chan"

    def setUp(self):
        # Default SIZE parameters. Can be overridden in test cases
        self.size_params = dict(
            ldim="2", lx1="8", lxd="12", lx2="lx1-0", lelg="96", lx1m="lx1", ldimt="3"
        )

        self.build_tools(["genmap"])
        self.run_genmap()

    @pn_pn_parallel
    def test_Std_ktau(self):
        self.config_size()
        self.build_nek()
        self.config_parfile({"GENERAL": {"userParam01": "4"}})
        self.config_parfile({"GENERAL": {"startFrom": "ktau.fld + time=0"}})
        self.run_nek(step_limit=None)

        xerr = self.get_value_from_log("u_tau", column=-1, row=-1)
        dnsval = 4.1487e-2
        relerr = abs(xerr-dnsval)/dnsval

        self.assertAlmostEqualDelayed(
            relerr, target_val=0.0, delta=1e-02, label="u_tau"
        )

        self.assertDelayedFailures()



    @pn_pn_parallel
    def test_Reg_komega(self):
        self.config_size()
        self.build_nek()
        self.config_parfile({"GENERAL": {"userParam01": "0"}})
        self.config_parfile({"GENERAL": {"startFrom": "komega.fld + time=0"}})
        self.run_nek(step_limit=None)

        xerr = self.get_value_from_log("u_tau", column=-1, row=-1)
        dnsval = 4.1487e-2
        relerr = abs(xerr-dnsval)/dnsval

        self.assertAlmostEqualDelayed(
            relerr, target_val=0.0, delta=1e-02, label="u_tau"
        )

        self.assertDelayedFailures()

###############################################################        


class Pipe(NekTestCase):
    example_subdir = "RANS_tests/Resolved/Pipe"
    case_name = "pipe"

    def setUp(self):
        # Default SIZE parameters. Can be overridden in test cases
        self.size_params = dict(
            ldim="3", lx1="8", lxd="12", lx2="lx1-0", lelg="4224", lx1m="lx1", ldimt="3", lpmin="2"
        )

        self.build_tools(["genmap"])
        self.run_genmap()

    @pn_pn_parallel
    def test_Std_ktau(self):
        self.config_size()
        self.build_nek()
        self.config_parfile({"GENERAL": {"userParam01": "4"}})
        self.config_parfile({"GENERAL": {"startFrom": "ktau.fld + time=0"}})
        self.run_nek(step_limit=None)

        xerr = self.get_value_from_log("u_tau", column=-1, row=-1)
        dnsval = 0.0530

        relerr = abs(xerr-dnsval)/dnsval

        self.assertAlmostEqualDelayed(
            relerr, target_val=0.0, delta=1e-02, label="u_tau"
        )

        self.assertDelayedFailures()



    @pn_pn_parallel
    def test_Reg_komega(self):
        self.config_size()
        self.build_nek()
        self.config_parfile({"GENERAL": {"userParam01": "0"}})
        self.config_parfile({"GENERAL": {"startFrom": "komega.fld + time=0"}})
        self.run_nek(step_limit=None)

        xerr = self.get_value_from_log("u_tau", column=-1, row=-1)
        dnsval = 0.0530
        relerr = abs(xerr-dnsval)/dnsval

        self.assertAlmostEqualDelayed(
            relerr, target_val=0.0, delta=1e-02, label="u_tau"
        )

        self.assertDelayedFailures()
        
        ###############################################################################

class WallChannel(NekTestCase):
    example_subdir = "RANS_tests/Wall_Function/Channel"
    case_name = "chan"

    def setUp(self):
        # Default SIZE parameters. Can be overridden in test cases
        self.size_params = dict(
            ldim="2", lx1="7", lxd="12", lx2="lx1-0", lelg="60", lx1m="lx1", ldimt="4", lhis="1001"
        )

        self.build_tools(["genmap"])
        self.run_genmap()

    @pn_pn_parallel
    def test_Std_ktau_pfalse(self):
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        xerr = self.get_value_from_log("u_tau", column=-1, row=-1)
        dnsval = 4.1487e-2
        relerr = abs(xerr-dnsval)/dnsval

        self.assertAlmostEqualDelayed(
            relerr, target_val=0.0, delta=7e-02, label="u_tau"
        )

        self.assertDelayedFailures()
        
###############################################################################

class WallPipe(NekTestCase):
    example_subdir = "RANS_tests/Wall_Function/Pipe"
    case_name = "pipe"

    def setUp(self):
        # Default SIZE parameters. Can be overridden in test cases
        self.size_params = dict(
            ldim="3", lx1="8", lxd="12", lx2="lx1-0", lelg="5000", lx1m="lx1", ldimt="6", lhis="1001"
        )

        self.build_tools(["genmap"])
        self.run_genmap()

    @pn_pn_parallel
    def test_Std_ktau(self):
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        xerr = self.get_value_from_log("u_tau", column=-1, row=-1)
        dnsval = 0.0530
        relerr = abs(xerr-dnsval)/dnsval

        self.assertAlmostEqualDelayed(
            relerr, target_val=0.0, delta=12e-02, label="u_tau"
        )

        self.assertDelayedFailures()
        
###############################################################################

class BFS(NekTestCase):
    example_subdir = "RANS_tests/Resolved/BackwardStep"
    case_name = "bfs"

    def setUp(self):
        # Default SIZE parameters. Can be overridden in test cases
        self.size_params = dict(
            ldim="2", lx1="8", lxd="12", lx2="lx1-0", lelg="6000", lx1m="lx1", ldimt="4", lhis="1001"
        )

        self.build_tools(["genmap"])
        self.run_genmap()

    @pn_pn_parallel
    def test_Std_ktau(self):
        self.config_size()
        self.config_parfile({"GENERAL": {"userParam01": "4"}})
        self.config_parfile({"GENERAL": {"startFrom": "ktau.fld + time=0"}})
        self.build_nek()
        
        self.run_nek(step_limit=None)
        
        xerr = self.get_value_from_log("r_l", column=-1, row=-1)
        ransval = 6.58
        expval = 6.26
        relerr_ex = abs(xerr*4-expval)/expval
        relerr_rans = abs(xerr*4-ransval)/ransval
        
        self.assertAlmostEqualDelayed(
            relerr_ex, target_val=0.0, delta=5e-02, label="Reattachment Length Experimental"
        )
        self.assertAlmostEqualDelayed(
            relerr_rans, target_val=0.0, delta=2e-02, label="Reattachment Length RANS (k_omega)"
        )
        
    @pn_pn_parallel
    def test_Std_komega(self):
        self.config_size()
        self.config_parfile({"GENERAL": {"userParam01": "0"}})
        self.config_parfile({"GENERAL": {"startFrom": "komega.fld + time=0"}})
        self.build_nek()
        
        self.run_nek(step_limit=None)
        
        xerr = self.get_value_from_log("r_l", column=-1, row=-1)
        ransval = 6.58
        expval = 6.26
        relerr_ex = abs(xerr*4-expval)/expval
        relerr_rans = abs(xerr*4-ransval)/ransval
        
        self.assertAlmostEqualDelayed(
            relerr_ex, target_val=0.0, delta=5e-02, label="Reattachment Length Experimental"
        )
        self.assertAlmostEqualDelayed(
            relerr_rans, target_val=0.0, delta=2e-02, label="Reattachment Length RANS (k_omega)"
        )

        self.assertDelayedFailures()
###############################################################################

class WallBFS(NekTestCase):
    example_subdir = "RANS_tests/Wall_Function/BackwardStep"
    case_name = "bfs"

    def setUp(self):
        # Default SIZE parameters. Can be overridden in test cases
        self.size_params = dict(
            ldim="2", lx1="6", lxd="12", lx2="lx1-0", lelg="4456", lx1m="lx1", ldimt="4", lhis="1001"
        )

        self.build_tools(["genmap"])
        self.run_genmap()

    @pn_pn_parallel
    def test_Std_ktau_pfalse(self):
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)

        xerr = self.get_value_from_log("r_l", column=-1, row=-1)
        ransval = 6.58
        expval = 6.26
        relerr_ex = abs(xerr*4-expval)/expval
        relerr_rans = abs(xerr*4-ransval)/ransval
        
        self.assertAlmostEqualDelayed(
            relerr_ex, target_val=0.0, delta=10e-02, label="Reattachment Length Experimental"
        )
        self.assertAlmostEqualDelayed(
            relerr_rans, target_val=0.0, delta=12e-02, label="Reattachment Length RANS (k_omega)"
        )

        self.assertDelayedFailures()

###############################################################        

class Dome(NekTestCase):
    example_subdir = "RANS_tests/Resolved/Dome"
    case_name = "TAMUdome"

    def setUp(self):
        # Default SIZE parameters. Can be overridden in test cases
        self.size_params = dict(
            ldim="2", lx1="9", lxd="12", lx2="lx1-0", lelg="3380", lx1m="lx1", ldimt="3", lhis="1001"
        )

        self.build_tools(["genmap"])
        self.run_genmap()

    @pn_pn_parallel
    def test_Std_ktau(self):
        self.config_size()
        self.build_nek()
        self.run_nek(step_limit=None)
        
        os.chdir("RANS_tests/Resolved/Dome/")

        subprocess.run(["python", "diff.py"])


        xerr = self.get_value_from_log("Max of L2 Norm of RANS to EXP : ", column=-1, row=-1) / 100
        
        self.assertAlmostEqualDelayed(
            xerr, target_val=0.0, delta=16e-02, label="Max L2 Norm"
        )

        self.assertDelayedFailures()
        
        
    ###############################################################
if __name__ == "__main__":
    import unittest
    import argparse

    # Get arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--f77",
        default="mpif77",
        help="The Fortran 77 compiler to use [default: mpif77]",
    )
    parser.add_argument(
        "--cc", default="mpicc", help="The C compiler to use [default: mpicc]"
    )
    parser.add_argument(
        "--ifmpi",
        default="true",
        choices=["true", "false"],
        help="Enable/disable parallel tests with MPI [default: true]",
    )
    parser.add_argument(
        "--nprocs",
        default="4",
        help="Number of processes to use for MPI tests [default: 4]",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    # # Set environment
    os.environ["CC"] = args.cc
    os.environ["FC"] = args.f77
    os.environ["IFMPI"] = args.ifmpi
    os.environ["PARALLEL_PROCS"] = args.nprocs
    if args.verbose:
        os.environ["VERBOSE_TESTS"] = "true"
        ut_verbose = 2
    else:
        os.environ["VERBOSE_TESTS"] = "false"
        ut_verbose = 1

    testList = (
        Tools,
        Channel,
        Pipe,
        BFS,
        WallChannel,
        WallPipe,
        WallBFS,
        Dome,
    )

    suite = unittest.TestSuite(
        [unittest.TestLoader().loadTestsFromTestCase(t) for t in testList]
    )
    unittest.TextTestRunner(verbosity=ut_verbose, buffer=True).run(suite)
    
    
