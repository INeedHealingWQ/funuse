#!/bin/csh
# Copyright (C) 2006 Aricent Inc . All Rights Reserved
# +--------------------------------------------------------------------------+
# |   FILE  NAME             : make.h                                        |
# |                                                                          |
# |   PRINCIPAL AUTHOR       : Aricent Inc.                               |
# |                                                                          |
# |   MAKE TOOL(S) USED      : GNU make                                      |
# |                                                                          |
# |   TARGET ENVIRONMENT     : LINUX                                         |
# |                                                                          |
# |   DATE                   : 22/08/2000                                    |
# |                                                                          |
# |   DESCRIPTION            : Specifies the options and modules to be       |
# |                            including for building the FutureLBD          |
# |                            product.                                      |
# |                                                                          |
# +--------------------------------------------------------------------------+
#
#     CHANGE RECORD :
# +--------------------------------------------------------------------------+
# | VERSION | AUTHOR/    | DESCRIPTION OF CHANGE                             |
# |         | DATE       |                                                   |
# +---------|------------|---------------------------------------------------+
# |   1     |            | Creation of makefile                              |
# +--------------------------------------------------------------------------+


include ../LR/make.h
include ../LR/make.rule


# Set the PROJ_BASE_DIR as the directory where you untar the project files
PROJECT_NAME		= FutureMain
PROJECT_BASE_DIR	= ${BASE_DIR}/wangtest
PROJECT_SOURCE_DIR	= ${PROJECT_BASE_DIR}/src
PROJECT_INCLUDE_DIR	= ${PROJECT_BASE_DIR}/inc
PROJECT_OBJECT_DIR	= ${PROJECT_BASE_DIR}/obj
PROJECT_MDL_DIR	    = ${PROJECT_BASE_DIR}/mdl

MD5_INCL_DIR        = ${BASE_DIR}/util/md5/inc


# Specify the project level compilation switches here
PROJECT_COMPILATION_SWITCHES = 


PROJECT_FINAL_INCLUDES_DIRS	= -I$(PROJECT_INCLUDE_DIR) \
					$(COMMON_INCLUDE_DIRS)
									


PROJECT_DEPENDENCIES	= $(COMMON_DEPENDENCIES) \
				$(PROJECT_FINAL_INCLUDE_FILES) \
				$(PROJECT_BASE_DIR)/Makefile \
				$(PROJECT_BASE_DIR)/make.h

ifeq (${SINGLE_IP_MANAGEMENT}, YES)
    INCLUDES += -I$(BASE_DIR)/sim/inc
endif
