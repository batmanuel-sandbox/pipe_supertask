#
# LSST Data Management System
# Copyright 2017 AURA/LSST.
#
# This product includes software developed by the
# LSST Project (http://www.lsst.org/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the LSST License Statement and
# the GNU General Public License along with this program.  If not,
# see <http://www.lsstcorp.org/LegalNotices/>.
#
"""
Module defining GraphBuilder class and related methods.
"""

from __future__ import print_function
from builtins import object

__all__ = ['GraphBuilder']

# -------------------------------
#  Imports of standard modules --
# -------------------------------
import copy

# -----------------------------
#  Imports for other modules --
# -----------------------------

# ----------------------------------
#  Local non-exported definitions --
# ----------------------------------

# ------------------------
#  Exported definitions --
# ------------------------


class GraphBuilder(object):
    """
    GraphBuilder class is responsible for building task execution graph from
    a Pipeline.

    Parameters
    ----------
    taskFactory : `TaskFactory`
        Factory object used to load/instantiate SuperTasks
    registry : :py:class:`daf.butler.Registry`
        Data butler instance.
    userQuery : `str`
        String which defunes user-defined selection for registry, should be
        empty or `None` if there is no restrictions on data selection.
    """

    def __init__(self, taskFactory, registry, userQuery):
        self.taskFactory = taskFactory
        self.registry = registry
        self.userQuery = userQuery

    def _loadTaskClass(self, taskDef):
        """Make sure task class is loaded.

        Load task class, update task name to make sure it is fully-qualified,
        do not update original taskDef in a Pipeline though.

        Parameters
        ----------
        taskDef : `TaskDef`

        Returns
        -------
        `TaskDef` instance, may be the same as parameter if task class is
        already loaded.
        """
        if taskDef.taskClass is None:
            tClass, tName = self.taskFactory.loadTaskClass(taskDef.taskName)
            taskDef = copy.copy(taskDef)
            taskDef.taskClass = tClass
            taskDef.taskName = tName
        return taskDef

    def makeGraph(self, pipeline):
        """Create execution graph for a pipeline.

        Parameters
        ----------
        pipeline : :py:class:`Pipeline`
            Pipeline definition, task names/classes and their configs.

        Returns
        -------
        :py:class:`QuantumGraph` instance.

        Raises
        ------
        Exceptions will be raised on errors.
        """

        # make sure all task classes are loaded
        taskList = [self._loadTaskClass(taskDef) for taskDef in pipeline]

        # build initial dataset graph
        inputs, outputs = self.buildIODatasets(taskList)

        # make a graph
        return self._makeGraph(taskList, inputs, outputs)

    def buildIODatasets(self, tasks):
        """Returns input and output dataset classes for all tasks.

        Parameters
        ----------
        tasks : sequence of `TaskDef`
            All tasks that form a pipeline.

        Returns
        -------
        inputs : set of `butler.core.datasets.DatasetType`
            Datasets used as inputs by the pipeline.
        outputs : set of `butler.core.datasets.DatasetType`
            Datasets produced by the pipeline.
        """
        # to build initial dataset graph we have to collect info about all
        # datasets to be used by this pipeline
        allDatasetTypes = {}
        inputs = set()
        outputs = set()
        for taskDef in tasks:
            taksClass = taskDef.taskClass
            taskInputs = taksClass.getInputDatasetTypes(taskDef.config)
            taskOutputs = taksClass.getOutputDatasetTypes(taskDef.config)
            if taskInputs:
                for dsType in taskInputs.values():
                    inputs.add(dsType.name)
                    allDatasetTypes[dsType.name] = dsType
            if taskOutputs:
                for dsType in taskOutputs.values():
                    outputs.add(dsType.name)
                    allDatasetTypes[dsType.name] = dsType

        # remove outputs from inputs
        inputs -= outputs

        inputs = set(allDatasetTypes[name] for name in inputs)
        outputs = set(allDatasetTypes[name] for name in outputs)
        return (inputs, outputs)

    def _makeGraph(self, tasks, inputs, outputs):
        """Make initial dataset graph instance.

        Parameters
        ----------
        tasks : sequence of `TaskDef`
            All tasks that form a pipeline.
        inputs : set of `DatasetType`
            Datasets which should already exist in input repository
        outputs : set of `DatasetType`
            Datasets which will be created by tasks

        Returns
        -------
        `QuantumGraph` instance.
        """

        # TODO: Actual implementation is needed
        graph = None
        return graph
