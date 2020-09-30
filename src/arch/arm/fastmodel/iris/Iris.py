# Copyright (c) 2020 ARM Limited
# All rights reserved.
#
# The license below extends only to copyright in the software and shall
# not be construed as granting a license to any other intellectual
# property including but not limited to intellectual property relating
# to a hardware implementation of the functionality of the software
# licensed hereunder.  You may use the software subject to the license
# terms below provided that you ensure that this notice is replicated
# unmodified and in its entirety in all distributions of the software,
# modified or unmodified, in source code or in binary form.
#
# Copyright 2019 Google, Inc.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from m5.params import *
from m5.proxy import *

from m5.objects.BaseCPU import BaseCPU
from m5.objects.BaseInterrupts import BaseInterrupts
from m5.objects.BaseISA import BaseISA
from m5.objects.BaseTLB import BaseTLB
from m5.objects.BaseMMU import BaseMMU

class IrisTLB(BaseTLB):
    type = 'IrisTLB'
    cxx_class = 'Iris::TLB'
    cxx_header = 'arch/arm/fastmodel/iris/tlb.hh'

class IrisMMU(BaseMMU):
    type = 'IrisMMU'
    cxx_class = 'Iris::MMU'
    cxx_header = 'arch/arm/fastmodel/iris/mmu.hh'
    itb = IrisTLB()
    dtb = IrisTLB()

class IrisInterrupts(BaseInterrupts):
    type = 'IrisInterrupts'
    cxx_class = 'Iris::Interrupts'
    cxx_header = 'arch/arm/fastmodel/iris/interrupts.hh'

class IrisISA(BaseISA):
    type = 'IrisISA'
    cxx_class = 'Iris::ISA'
    cxx_header = 'arch/arm/fastmodel/iris/isa.hh'

class IrisBaseCPU(BaseCPU):
    type = 'IrisBaseCPU'
    abstract = True
    cxx_class = 'Iris::BaseCPU'
    cxx_header = 'arch/arm/fastmodel/iris/cpu.hh'

    @classmethod
    def memory_mode(cls):
        return 'atomic_noncaching'

    @classmethod
    def require_caches(cls):
        return False

    @classmethod
    def support_take_over(cls):
        #TODO Make this work.
        return False

    evs = Param.SystemC_ScModule(
            "Fast model exported virtual subsystem holding cores")
    thread_paths = VectorParam.String(
            "Sub-paths to elements in the EVS which support a thread context")

    dtb = IrisTLB()
    itb = IrisTLB()

    def createThreads(self):
        if len(self.isa) == 0:
            self.isa = [ IrisISA() for i in range(self.numThreads) ]
        else:
            assert(len(self.isa) == int(self.numThreads))

    def createInterruptController(self):
        self.interrupts = [ IrisInterrupts() for i in range(self.numThreads) ]
