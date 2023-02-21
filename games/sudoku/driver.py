#
# Copyright (C) 2022 Vaticle
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import timeit
from sys import argv

from solver import Solver
from typedb.client import TypeDB

HOST = TypeDB.DEFAULT_ADDRESS
DATABASE_NAME = "sudoku6x6"

def main():
    if len(argv) != 2:
        print("Usage:")
        print("python3 %s setup:            Loads required schema & data" % argv[0])
        print("python3 %s <sudoku_file>:    Reads & solves the sudoku in <sudoku_file>" % argv[0])
        return

    solver = Solver(HOST, DATABASE_NAME)
    if argv[1] == "setup":
        solver.setup(force=True)
        return

    solver.setup()
    sudoku = solver.read_sudoku(argv[1])

    print("Solving:")
    print(solver.format_sudoku(sudoku), "\n")

    time_start = timeit.default_timer()
    solution = solver.solve(sudoku)
    time_taken_ms = int((timeit.default_timer() - time_start) * 1000 + 1)
    if solution:
        print("Found solution in " + str(time_taken_ms) + " ms:")
        print(solver.format_sudoku(solution))
    else:
        print("No solution (took " + str(time_taken_ms) + " ms)")

    solver.cleanup()

if __name__=="__main__": main()
