# generated by datamodel-codegen:
#   filename:  openapi.json
#   timestamp: 2024-01-04T10:55:22+00:00

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID

from pydantic import BaseModel, Extra, Field, PositiveFloat, confloat, conint, RootModel


class User(BaseModel):
    name: Optional[str] = Field('User', description='Name of the user')
    about: Optional[str] = Field(None, description='About the user')
    created_at: Optional[datetime] = Field(
        None, description='User created at (RFC-3339 format)'
    )
    updated_at: Optional[datetime] = Field(
        None, description='User updated at (RFC-3339 format)'
    )
    id: UUID = Field(..., description='User id (UUID)')


class FunctionParameters(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class FunctionDef(BaseModel):
    description: Optional[str] = Field(
        None,
        description='A description of what the function does, used by the model to choose when and how to call the function.',
    )
    name: str = Field(
        ...,
        description='The name of the function to be called. Must be a-z, A-Z, 0-9, or contain underscores and dashes, with a maximum length of 64.',
    )
    parameters: FunctionParameters = Field(
        ..., description='Parameters accepeted by this function'
    )


class Type(Enum):
    function = 'function'
    webhook = 'webhook'


class Tool(BaseModel):
    type: Type = Field(
        ...,
        description='Whether this tool is a `function` or a `webhook` (Only `function` tool supported right now)',
    )
    definition: FunctionDef = Field(
        ..., description='Function definition and parameters'
    )


class Session(BaseModel):
    id: UUID = Field(..., description='Session id (UUID)')
    user_id: UUID = Field(
        ..., description='User ID of user associated with this session'
    )
    agent_id: UUID = Field(
        ..., description='Agent ID of agent associated with this session'
    )
    situation: Optional[str] = Field(
        None,
        description='A specific situation that sets the background for this session',
    )
    summary: Optional[str] = Field(
        None,
        description='(null at the beginning) - generated automatically after every interaction',
    )
    created_at: Optional[datetime] = Field(
        None, description='Session created at (RFC-3339 format)'
    )
    updated_at: Optional[datetime] = Field(
        None, description='Session updated at (RFC-3339 format)'
    )


class CreateSessionRequest(BaseModel):
    user_id: str = Field(
        ..., description='User ID of user to associate with this session'
    )
    agent_id: str = Field(
        ..., description='Agent ID of agent to associate with this session'
    )
    situation: Optional[str] = Field(
        None,
        description='A specific situation that sets the background for this session',
    )


class UpdateSessionRequest(BaseModel):
    situation: str = Field(..., description='Updated situation for this session')


class UpdateUserRequest(BaseModel):
    about: Optional[str] = Field(None, description='About the user')
    name: Optional[str] = Field(None, description='Name of the user')


class Target(Enum):
    user = 'user'
    agent = 'agent'


class Suggestion(BaseModel):
    created_at: Optional[datetime] = Field(
        None, description='Suggestion created at (RFC-3339 format)'
    )
    target: Target = Field(
        ..., description='Whether the suggestion is for the `agent` or a `user`'
    )
    content: str = Field(..., description='The content of the suggestion')
    message_id: UUID = Field(..., description='The message that produced it')
    session_id: UUID = Field(..., description='Session this suggestion belongs to')


class Role(str, Enum):
    user = 'user'
    assistant = 'assistant'
    system = 'system'
    function_call = 'function_call'


class ChatMLMessage(BaseModel):
    role: Role = Field(
        ..., description='ChatML role (system|assistant|user|function_call)'
    )
    content: str = Field(..., description='ChatML content')
    name: Optional[str] = Field(None, description='ChatML name')
    created_at: datetime = Field(
        ..., description='Message created at (RFC-3339 format)'
    )
    id: UUID = Field(..., description='Message ID')


class InputChatMLMessage(BaseModel):
    role: Role = Field(
        ..., description='ChatML role (system|assistant|user|function_call)'
    )
    content: str = Field(..., description='ChatML content')
    name: Optional[str] = Field(None, description='ChatML name')
    continue_: Optional[bool] = Field(
        False,
        alias='continue',
        description='Whether to continue this message or return a new one',
    )


class Type1(Enum):
    function = 'function'


class Function(BaseModel):
    name: str = Field(..., description='The name of the function to call.')


class NamedToolChoice(BaseModel):
    type: Type1 = Field(
        ...,
        description='The type of the tool. Currently, only `function` is supported.',
    )
    function: Function


class ToolChoiceOption1(Enum):
    none = 'none'
    auto = 'auto'


class ToolChoiceOption(RootModel):
    root: Union[ToolChoiceOption1, NamedToolChoice] = Field(
        ...,
        description='Controls which (if any) function is called by the model.\n`none` means the model will not call a function and instead generates a message.\n`auto` means the model can pick between generating a message or calling a function.\nSpecifying a particular function via `{"type: "function", "function": {"name": "my_function"}}` forces the model to call that function.\n\n`none` is the default when no functions are present. `auto` is the default if functions are present.\n',
    )


class FunctionCallOption(BaseModel):
    name: str = Field(..., description='The name of the function to call.')


class CompletionUsage(BaseModel):
    completion_tokens: int = Field(
        ..., description='Number of tokens in the generated completion.'
    )
    prompt_tokens: int = Field(..., description='Number of tokens in the prompt.')
    total_tokens: int = Field(
        ...,
        description='Total number of tokens used in the request (prompt + completion).',
    )


class FinishReason(Enum):
    stop = 'stop'
    length = 'length'
    tool_calls = 'tool_calls'
    content_filter = 'content_filter'
    function_call = 'function_call'


class Response(BaseModel):
    items: Optional[ChatMLMessage] = None


class ChatResponse(BaseModel):
    id: UUID = Field(..., description='A unique identifier for the chat completion.')
    finish_reason: FinishReason = Field(
        ...,
        description='The reason the model stopped generating tokens. This will be `stop` if the model hit a natural stop point or a provided stop sequence, `length` if the maximum number of tokens specified in the request was reached, `content_filter` if content was omitted due to a flag from our content filters, `tool_calls` if the model called a tool, or `function_call` (deprecated) if the model called a function.',
    )
    response: List[Union[List[ChatMLMessage], Response]] = Field(
        ..., description='A list of chat completion messages produced as a response.'
    )
    usage: CompletionUsage


class Type2(Enum):
    belief = 'belief'


class Belief(BaseModel):
    type: Type2 = Field(..., description='Type of memory (`belief`)')
    subject: Optional[UUID] = Field(
        None, description='(Optional) ID of the subject user'
    )
    content: str = Field(..., description='Content of the memory')
    rationale: Optional[str] = Field(
        None, description='Rationale: Why did the model decide to form this memory'
    )
    weight: confloat(lt=100.0, gt=0.0) = Field(
        ..., description='Weight (importance) of the memory on a scale of 0-100'
    )
    sentiment: confloat(lt=1.0, gt=-1.0) = Field(
        ..., description='Sentiment (valence) of the memory on a scale of -1 to 1'
    )
    created_at: datetime = Field(..., description='Belief created at (RFC-3339 format)')
    id: UUID = Field(..., description='Belief id (UUID)')


class Type3(Enum):
    episode = 'episode'


class Episode(BaseModel):
    type: Type3 = Field(..., description='Type of memory (`episode`)')
    subject: Optional[UUID] = Field(
        None, description='(Optional) ID of the subject user'
    )
    content: str = Field(..., description='Content of the memory')
    weight: confloat(lt=100.0, gt=0.0) = Field(
        ..., description='Weight (importance) of the memory on a scale of 0-100'
    )
    created_at: datetime = Field(
        ..., description='Episode created at (RFC-3339 format)'
    )
    last_accessed_at: datetime = Field(
        ..., description='Episode last accessed at (RFC-3339 format)'
    )
    happened_at: datetime = Field(
        ..., description='Episode happened at (RFC-3339 format)'
    )
    duration: Optional[PositiveFloat] = Field(
        0, description='Duration of the episode (in seconds)'
    )
    id: UUID = Field(..., description='Episode id (UUID)')


class Entity(BaseModel):
    id: UUID = Field(..., description='Entity id (UUID)')


class Type4(Enum):
    text = 'text'
    json_object = 'json_object'


class ResponseFormat(BaseModel):
    type: Optional[Type4] = Field(
        'text',
        description='Must be one of `text` or `json_object`.',
        example='json_object',
    )


class ChatSettings(BaseModel):
    frequency_penalty: Optional[confloat(ge=-1.0, le=1.0)] = Field(
        0,
        description="(OpenAI-like) Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
    length_penalty: Optional[confloat(ge=0.0, le=2.0)] = Field(
        1,
        description='(Huggingface-like) Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize number of tokens generated. ',
    )
    logit_bias: Optional[Dict[str, int]] = Field(
        None,
        description='Modify the likelihood of specified tokens appearing in the completion.\n\nAccepts a JSON object that maps tokens (specified by their token ID in the tokenizer) to an associated bias value from -100 to 100. Mathematically, the bias is added to the logits generated by the model prior to sampling. The exact effect will vary per model, but values between -1 and 1 should decrease or increase likelihood of selection; values like -100 or 100 should result in a ban or exclusive selection of the relevant token.\n',
    )
    max_tokens: Optional[int] = Field(
        None,
        description="The maximum number of tokens to generate in the chat completion.\n\nThe total length of input tokens and generated tokens is limited by the model's context length.\n",
    )
    presence_penalty: Optional[confloat(ge=-1.0, le=1.0)] = Field(
        0,
        description="(OpenAI-like) Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
    repetition_penalty: Optional[confloat(ge=0.0, le=2.0)] = Field(
        1,
        description="(Huggingface-like) Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
    response_format: Optional[ResponseFormat] = Field(
        None,
        description='An object specifying the format that the model must output.\n\nSetting to `{ "type": "json_object" }` enables JSON mode, which guarantees the message the model generates is valid JSON.\n\n**Important:** when using JSON mode, you **must** also instruct the model to produce JSON yourself via a system or user message. Without this, the model may generate an unending stream of whitespace until the generation reaches the token limit, resulting in a long-running and seemingly "stuck" request. Also note that the message content may be partially cut off if `finish_reason="length"`, which indicates the generation exceeded `max_tokens` or the conversation exceeded the max context length.\n',
    )
    seed: Optional[conint(ge=-9223372036854776000, le=9223372036854776000)] = Field(
        None,
        description='This feature is in Beta.\nIf specified, our system will make a best effort to sample deterministically, such that repeated requests with the same `seed` and parameters should return the same result.\nDeterminism is not guaranteed, and you should refer to the `system_fingerprint` response parameter to monitor changes in the backend.\n',
    )
    stop: Optional[Union[str, List[str]]] = Field(
        None,
        description='Up to 4 sequences where the API will stop generating further tokens.\n',
    )
    stream: bool = Field(
        ...,
        description='If set, partial message deltas will be sent, like in ChatGPT. Tokens will be sent as data-only [server-sent events](https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events/Using_server-sent_events#Event_stream_format) as they become available, with the stream terminated by a `data: [DONE]` message. [Example Python code](https://cookbook.openai.com/examples/how_to_stream_completions).\n',
    )
    temperature: Optional[confloat(ge=0.0, le=2.0)] = Field(
        1,
        description='What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.',
        example=1,
    )
    top_p: Optional[confloat(ge=0.0, le=1.0)] = Field(
        1,
        description='Defaults to 1 An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.  We generally recommend altering this or temperature but not both.',
        example=1,
    )


class AgentDefaultSettings(BaseModel):
    frequency_penalty: Optional[confloat(lt=2.0, gt=-2.0)] = Field(
        0,
        description="(OpenAI-like) Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
    length_penalty: Optional[confloat(ge=0.0, le=2.0)] = Field(
        1,
        description='(Huggingface-like) Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize number of tokens generated. ',
    )
    presence_penalty: Optional[confloat(ge=-1.0, le=1.0)] = Field(
        0,
        description="(OpenAI-like) Number between -2.0 and 2.0. Positive values penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
    repetition_penalty: Optional[confloat(ge=0.0, le=2.0)] = Field(
        1,
        description="(Huggingface-like) Number between 0 and 2.0. 1.0 is neutral and values larger than that penalize new tokens based on their existing frequency in the text so far, decreasing the model's likelihood to repeat the same line verbatim.",
    )
    temperature: Optional[confloat(ge=0.0, le=2.0)] = Field(
        1,
        description='What sampling temperature to use, between 0 and 2. Higher values like 0.8 will make the output more random, while lower values like 0.2 will make it more focused and deterministic.',
        example=1,
    )
    top_p: Optional[confloat(ge=0.0, le=1.0)] = Field(
        1,
        description='Defaults to 1 An alternative to sampling with temperature, called nucleus sampling, where the model considers the results of the tokens with top_p probability mass. So 0.1 means only the tokens comprising the top 10% probability mass are considered.  We generally recommend altering this or temperature but not both.',
        example=1,
    )


class AdditionalInfo(BaseModel):
    title: str = Field(
        ..., description='Title describing what this bit of information contains'
    )
    content: str = Field(..., description='Information content')
    id: str = Field(..., description='ID of additional info doc')


class CreateAdditionalInfoRequest(BaseModel):
    title: str = Field(
        ..., description='Title describing what this bit of information contains'
    )
    content: str = Field(..., description='Information content')


class MemoryAccessOptions(BaseModel):
    recall: Optional[bool] = Field(
        True, description='Whether previous memories should be recalled or not'
    )
    remember: Optional[bool] = Field(
        True, description='Whether this interaction should be recorded in memory or not'
    )


class Agent(BaseModel):
    name: str = Field(..., description='Name of the agent')
    about: str = Field(..., description='About the agent')
    instructions: Optional[List[str]] = Field(
        None, description='List of instructions for the agent'
    )
    created_at: Optional[datetime] = Field(
        None, description='Agent created at (RFC-3339 format)'
    )
    updated_at: Optional[datetime] = Field(
        None, description='Agent updated at (RFC-3339 format)'
    )
    tools: Optional[List[Tool]] = Field(
        None,
        description='A list of tools the model may call. Currently, only `function`s are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for.',
    )
    id: UUID = Field(..., description='Agent id (UUID)')
    default_settings: Optional[AgentDefaultSettings] = Field(
        None, description='Default settings for all sessions created by this agent'
    )
    model: str = Field(..., description='The model to use with this agent')


class CreateUserRequest(BaseModel):
    name: Optional[str] = Field('User', description='Name of the user')
    about: Optional[str] = Field(None, description='About the user')
    additional_information: Optional[List[CreateAdditionalInfoRequest]] = Field(
        None, description='List of additional info about user'
    )


class CreateAgentRequest(BaseModel):
    name: str = Field(..., description='Name of the agent')
    about: str = Field(..., description='About the agent')
    instructions: Optional[List[str]] = Field(
        None, description='List of instructions for the agent'
    )
    tools: Optional[List[Tool]] = Field(
        None,
        description='A list of tools the model may call. Currently, only `function`s are supported as a tool. Use this to provide a list of functions the model may generate JSON inputs for.',
    )
    default_settings: Optional[AgentDefaultSettings] = Field(
        None, description='Default model settings to start every session with'
    )
    model: str = Field(
        ..., description='Name of the model that the agent is supposed to use'
    )
    additional_info: Optional[List[CreateAdditionalInfoRequest]] = Field(
        None, description='List of additional info about agent'
    )


class UpdateAgentRequest(BaseModel):
    about: Optional[str] = Field(None, description='About the agent')
    instructions: Optional[List[str]] = Field(
        None, description='List of instructions for the agent'
    )
    tools: Optional[List[Tool]] = Field(
        None, description='List of tools available to this agent'
    )
    name: Optional[str] = Field(None, description='Name of the agent')
    model: Optional[str] = Field(
        None, description='Name of the model that the agent is supposed to use'
    )
    default_settings: Optional[AgentDefaultSettings] = Field(
        None, description='Default model settings to start every session with'
    )


class ChatInputData(BaseModel):
    messages: List[InputChatMLMessage] = Field(
        ...,
        description='A list of new input messages comprising the conversation so far.',
        min_items=1,
    )
    tools: Optional[List[Tool]] = Field(
        None,
        description="(Advanced) List of tools that are provided in addition to agent's default set of tools. Functions of same name in agent set are overriden",
    )
    tool_choice: Optional[ToolChoiceOption] = Field(
        None,
        description='Can be one of existing tools given to the agent earlier or the ones included in the request',
    )


class Memory(RootModel):
    root: Union[Belief, Episode, Entity]


class ChatInput(ChatInputData, ChatSettings, MemoryAccessOptions):
    pass
