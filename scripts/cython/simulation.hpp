#ifndef SIM_PAR
#define SIM_PAR
#include "mpi.h"
#include "process.hpp"
#include <utility>
int get_rank();
int get_comm_size();
void parallele_simulation(Process *process);
#endif