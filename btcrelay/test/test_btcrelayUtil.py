from pyethereum import tester

import pytest
slow = pytest.mark.slow

class TestBtcRelayUtil(object):

    CONTRACT = 'btcrelayUtil.py'
    CONTRACT_GAS = 55000

    ETHER = 10 ** 18

    def setup_class(cls):
        cls.s = tester.state()
        cls.c = cls.s.abi_contract(cls.CONTRACT, endowment=2000*cls.ETHER)
        cls.snapshot = cls.s.snapshot()
        cls.seed = tester.seed

    def setup_method(self, method):
        self.s.revert(self.snapshot)
        tester.seed = self.seed


    def testComputeMerkle(self):
        # values are from block 100K
        tx = 0x8c14f0db3df150123e6f3dbbf30f8b955a8249b62ac1d1ff16284aefa3d06d87
        proofLen = 2
        hash = [None] * proofLen
        path = [None] * proofLen

        RIGHT_HASH = 2  # from btcrelay.py

        hash[0] = 0xfff2525b8931402dd09222c50775608f75787bd2b87e56995a7bdd30f79702c4
        path[0] = RIGHT_HASH

        hash[1] = 0x8e30899078ca1813be036a073bbf80b86cdddde1c96e9e9c99e9e3782df4ae49
        path[1] = RIGHT_HASH

        r = self.c.computeMerkle(tx, proofLen, hash, path)
        r %= 2**256
        expMerkle = 0xf3e94742aca4b5ef85488dc37c06c3282295ffec960994b2c0d5ac2a25a95766
        assert r == expMerkle


    def testHashBlock100K(self):
        blockHeaderStr = "0100000050120119172a610421a6c3011dd330d9df07b63616c2cc1f1cd00200000000006657a9252aacd5c0b2940996ecff952228c3067cc38d4885efb5a4ac4247e9f337221b4d4c86041b0f2b5710"
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.fastHashBlock(bhBinary)
        exp = 0x000000000003ba27aa200b1cecaad478d2b00432346c3f1f3986da1afd33e506
        assert res == exp


    def testHashBlock300K(self):
        blockHeaderStr = "020000007ef055e1674d2e6551dba41cd214debbee34aeb544c7ec670000000000000000d3998963f80c5bab43fe8c26228e98d030edf4dcbe48a666f5c39e2d7a885c9102c86d536c890019593a470d"
        bhBinary = blockHeaderStr.decode('hex')
        res = self.c.fastHashBlock(bhBinary)
        exp = 0x000000000000000082ccf8f1557c5d40b21edabb18d2d691cfbf87118bac7254
        assert res == exp
