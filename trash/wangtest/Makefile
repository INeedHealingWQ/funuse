#!/bin/csh
# Copyright (C) 2006 Aricent Inc . All Rights Reserved
#----------------------------------------------------------------------------+
# |   FILE  NAME             : FutureMACNOTIFY.mak                            |
# |                                                                          |
# |   PRINCIPAL AUTHOR       : Aricent Inc.                                  |
# |                                                                          |
# |   MAKE TOOL(S) USED      : GNU MAKE                                      |
# |                                                                          |
# |   TARGET ENVIRONMENT     : LINUX                                         |
# |                                                                          |
# |   DATE                   : 10h December 2005                             |
# |   DESCRIPTION            : This makefile is used to build the            |
# |                            FutureMACNOTIFY module.                       |
# +--------------------------------------------------------------------------+
#

#include the Product make.h
include ../LR/make.h
include ../LR/make.rule
include make.h

# Build Output Files

################### Project/Module Object Files(s) ####################
# Project/Module Object Files(s)
PROJECT_OBJECT_LIST	= ${PROJECT_OBJECT_DIR}/main.o

PROJECT_FINAL_OBJ = $(PROJECT_OBJECT_DIR)/$(PROJECT_NAME).o

#######################################################################

$(PROJECT_FINAL_OBJ) : obj $(PROJECT_OBJECT_LIST)
	$(LD) $(LD_FLAGS) -o $(PROJECT_FINAL_OBJ)  ${PROJECT_OBJECT_LIST}

obj :
	$(MKDIR)  $(MKDIR_FLAGS) obj

clean :
	@echo "Cleaning Mac Notify object files"
	$(RM)  $(RM_FLAGS) obj/*.o


############################################################################
#  The rules required for the compilation of the individual Object files   #
############################################################################


${PROJECT_OBJECT_DIR}/main.o: $(PROJECT_SOURCE_DIR)/main.c $(PROJECT_DEPENDENCIES)
	${CC} $(CC_FLAGS) $(GENERAL_COMPILATION_SWITCHES)           \
	                  $(SYSTEM_COMPILATION_SWITCHES)            \
	                  $(PROJECT_COMPILATION_SWITCHES)           \
	                  $(PROJECT_FINAL_INCLUDES_DIRS)            \
                      $(PROJECT_SOURCE_DIR)/main.c -o        \
	                  $(PROJECT_OBJECT_DIR)/main.o

