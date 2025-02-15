# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

# pylint: disable=no-self-use

import logging
from typing import Any

from marshmallow import fields, post_load

from azure.ai.ml._schema import ArmVersionedStr, PatchedSchemaMeta, RegistryStr, StringTransformedEnum, UnionField
from azure.ai.ml._schema.pipeline.pipeline_component import PipelineComponentFileRefField
from azure.ai.ml.constants._common import AzureMLResourceType
from azure.ai.ml.constants._job.job import JobType

module_logger = logging.getLogger(__name__)


class JobDefinitionSchema(metaclass=PatchedSchemaMeta):
    component_id = fields.Str()
    job = UnionField(
        [
            RegistryStr(azureml_type=AzureMLResourceType.JOB),
            PipelineComponentFileRefField(),
        ]
    )
    component = UnionField(
        [
            ArmVersionedStr(azureml_type=AzureMLResourceType.COMPONENT, allow_default_version=True),
            PipelineComponentFileRefField(),
        ]
    )
    type = StringTransformedEnum(required=True, allowed_values=[JobType.PIPELINE])
    settings = fields.Dict()
    name = fields.Str()
    description = fields.Str()
    tags = fields.Dict()

    @post_load
    def make(self, data: Any, **kwargs: Any) -> Any:  # pylint: disable=unused-argument
        from azure.ai.ml.entities._deployment.job_definition import JobDefinition

        return JobDefinition(**data)
