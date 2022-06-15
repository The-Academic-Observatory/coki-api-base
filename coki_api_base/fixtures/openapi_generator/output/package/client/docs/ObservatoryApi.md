# ObservatoryApi

All URIs are relative to *https://ao-api.observatory.academy*

<div class="wy-table-responsive"><table border="1" class="docutils">
<thead>
<tr>
<th>Method</th>
<th>HTTP request</th>
<th>Description</th>
</tr>
</thead>
<tbody>


<tr>
  <td><a href="ObservatoryApi.html#pit_id_agg"><strong>pit_id_agg</strong></a></td>
  <td><strong>GET</strong> /v1/{agg}/pit</td>
  <td></td>
</tr>

<tr>
  <td><a href="ObservatoryApi.html#pit_id_subagg"><strong>pit_id_subagg</strong></a></td>
  <td><strong>GET</strong> /v1/{agg}/{subagg}/pit</td>
  <td></td>
</tr>

<tr>
  <td><a href="ObservatoryApi.html#query_agg"><strong>query_agg</strong></a></td>
  <td><strong>GET</strong> /v1/{agg}</td>
  <td></td>
</tr>

<tr>
  <td><a href="ObservatoryApi.html#query_subagg"><strong>query_subagg</strong></a></td>
  <td><strong>GET</strong> /v1/{agg}/{subagg}</td>
  <td></td>
</tr>


</tbody>
</table></div>

## **pit_id_agg**
> PitResponse pit_id_agg(agg)



### Example

* Api Key Authentication (api_key):
```python
import time
import package.client
from package.client.api import observatory_api
from package.client.model.pit_response import PitResponse
from pprint import pprint
# Defining the host is optional and defaults to https://ao-api.observatory.academy
# See configuration.py for a list of all supported configuration parameters.
configuration = package.client.Configuration(
    host = "https://ao-api.observatory.academy"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with package.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = observatory_api.ObservatoryApi(api_client)
    agg = "author" # str | The aggregate.
    index_date = dateutil_parser('1970-01-01').date() # date | Index date, defaults to latest (optional)
    keep_alive = 1 # int | How long to keep the point in time id alive (in minutes)  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.pit_id_agg(agg)
        pprint(api_response)
    except package.client.ApiException as e:
        print("Exception when calling ObservatoryApi->pit_id_agg: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.pit_id_agg(agg, index_date=index_date, keep_alive=keep_alive)
        pprint(api_response)
    except package.client.ApiException as e:
        print("Exception when calling ObservatoryApi->pit_id_agg: %s\n" % e)
```


### Parameters


<div class="wy-table-responsive"><table border="1" class="docutils">
<thead>
<tr>
<th>Name</th>
<th>Type</th>
<th>Description</th>
<th>Notes</th>
</tr>
</thead>
<tbody>



<tr>
<td><strong>agg</strong></td>
<td><strong>str</strong></td>
<td>The aggregate.</td>
<td></td>
</tr>




<tr>
<td><strong>index_date</strong></td>
<td><strong>date</strong></td>
<td>Index date, defaults to latest</td>
<td>
[optional]
<tr>
<td><strong>keep_alive</strong></td>
<td><strong>int</strong></td>
<td>How long to keep the point in time id alive (in minutes) </td>
<td>
[optional]
</tbody>
</table></div>


### Return type

[**PitResponse**](PitResponse.html)

### Authorization

[api_key](ObservatoryApi.html#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
<div class="wy-table-responsive"><table border="1" class="docutils">
<thead>
<tr>
<th>Status code</th>
<th>Description</th>
<th>Response headers</th>
</tr>
</thead>
<tbody>

<tr>
    <td><strong>200</strong></td>
    <td>Create a new pit id for the specified aggregate. When creating a Point In Time the current index state is preserved for a limited time. This specific state can be used by passing on the pit id as a parameter to the search request. Each search request can return a different id; thus always use the most recently received id for the next search request. </td>
    <td> - </td>
</tr>
<tr>
    <td><strong>401</strong></td>
    <td>API key is missing or invalid</td>
    <td> * WWW_Authenticate -  <br> </td>
</tr>

</tbody>
</table></div>

## **pit_id_subagg**
> PitResponse pit_id_subagg(agg, subagg)



### Example

* Api Key Authentication (api_key):
```python
import time
import package.client
from package.client.api import observatory_api
from package.client.model.pit_response import PitResponse
from pprint import pprint
# Defining the host is optional and defaults to https://ao-api.observatory.academy
# See configuration.py for a list of all supported configuration parameters.
configuration = package.client.Configuration(
    host = "https://ao-api.observatory.academy"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with package.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = observatory_api.ObservatoryApi(api_client)
    agg = "author" # str | The aggregate.
    subagg = "access-types" # str | The sub-aggregate.
    index_date = dateutil_parser('1970-01-01').date() # date | Index date, defaults to latest (optional)
    keep_alive = 1 # int | How long to keep the point in time id alive (in minutes)  (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.pit_id_subagg(agg, subagg)
        pprint(api_response)
    except package.client.ApiException as e:
        print("Exception when calling ObservatoryApi->pit_id_subagg: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.pit_id_subagg(agg, subagg, index_date=index_date, keep_alive=keep_alive)
        pprint(api_response)
    except package.client.ApiException as e:
        print("Exception when calling ObservatoryApi->pit_id_subagg: %s\n" % e)
```


### Parameters


<div class="wy-table-responsive"><table border="1" class="docutils">
<thead>
<tr>
<th>Name</th>
<th>Type</th>
<th>Description</th>
<th>Notes</th>
</tr>
</thead>
<tbody>



<tr>
<td><strong>agg</strong></td>
<td><strong>str</strong></td>
<td>The aggregate.</td>
<td></td>
</tr>

<tr>
<td><strong>subagg</strong></td>
<td><strong>str</strong></td>
<td>The sub-aggregate.</td>
<td></td>
</tr>





<tr>
<td><strong>index_date</strong></td>
<td><strong>date</strong></td>
<td>Index date, defaults to latest</td>
<td>
[optional]
<tr>
<td><strong>keep_alive</strong></td>
<td><strong>int</strong></td>
<td>How long to keep the point in time id alive (in minutes) </td>
<td>
[optional]
</tbody>
</table></div>


### Return type

[**PitResponse**](PitResponse.html)

### Authorization

[api_key](ObservatoryApi.html#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
<div class="wy-table-responsive"><table border="1" class="docutils">
<thead>
<tr>
<th>Status code</th>
<th>Description</th>
<th>Response headers</th>
</tr>
</thead>
<tbody>

<tr>
    <td><strong>200</strong></td>
    <td>Create a new pit id for the specified aggregate and subaggregate. When creating a Point In Time the current index state is preserved for a limited time. This specific state can be used by passing on the pit id as a parameter to the search request. Each search request can return a different id; thus always use the most recently received id for the next search request. </td>
    <td> - </td>
</tr>
<tr>
    <td><strong>401</strong></td>
    <td>API key is missing or invalid</td>
    <td> * WWW_Authenticate -  <br> </td>
</tr>

</tbody>
</table></div>

## **query_agg**
> QueryResponse query_agg(agg)



### Example

* Api Key Authentication (api_key):
```python
import time
import package.client
from package.client.api import observatory_api
from package.client.model.query_response import QueryResponse
from pprint import pprint
# Defining the host is optional and defaults to https://ao-api.observatory.academy
# See configuration.py for a list of all supported configuration parameters.
configuration = package.client.Configuration(
    host = "https://ao-api.observatory.academy"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with package.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = observatory_api.ObservatoryApi(api_client)
    agg = "author" # str | The aggregate.
    agg_id = [
        "agg_id_example",
    ] # [str] | Filter on aggregates with this id, if multiple values are given the results are filtered on whether there are aggregates with one of the given values.  (optional)
    index_date = dateutil_parser('1970-01-01').date() # date | Index date, defaults to latest (optional)
    _from = dateutil_parser('1970-01-01').date() # date | Start year (included) (optional)
    to = dateutil_parser('1970-01-01').date() # date | End year (included) (optional)
    limit = 1 # int | Limit number of results (max 10000) (optional)
    search_after = "search_after_example" # str | The sort value of the last item from the previous search, used to paginate. The results are sorted by _shard_doc when a PIT is used and by document id (_id) without a PIT.  (optional)
    pit = "pit_example" # str | The pit id (optional)
    pretty = True # bool | If true, the endpoint returns only the user metadata. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.query_agg(agg)
        pprint(api_response)
    except package.client.ApiException as e:
        print("Exception when calling ObservatoryApi->query_agg: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.query_agg(agg, agg_id=agg_id, index_date=index_date, _from=_from, to=to, limit=limit, search_after=search_after, pit=pit, pretty=pretty)
        pprint(api_response)
    except package.client.ApiException as e:
        print("Exception when calling ObservatoryApi->query_agg: %s\n" % e)
```


### Parameters


<div class="wy-table-responsive"><table border="1" class="docutils">
<thead>
<tr>
<th>Name</th>
<th>Type</th>
<th>Description</th>
<th>Notes</th>
</tr>
</thead>
<tbody>



<tr>
<td><strong>agg</strong></td>
<td><strong>str</strong></td>
<td>The aggregate.</td>
<td></td>
</tr>




<tr>
<td><strong>agg_id</strong></td>
<td><strong>[str]</strong></td>
<td>Filter on aggregates with this id, if multiple values are given the results are filtered on whether there are aggregates with one of the given values. </td>
<td>
[optional]
<tr>
<td><strong>index_date</strong></td>
<td><strong>date</strong></td>
<td>Index date, defaults to latest</td>
<td>
[optional]
<tr>
<td><strong>_from</strong></td>
<td><strong>date</strong></td>
<td>Start year (included)</td>
<td>
[optional]
<tr>
<td><strong>to</strong></td>
<td><strong>date</strong></td>
<td>End year (included)</td>
<td>
[optional]
<tr>
<td><strong>limit</strong></td>
<td><strong>int</strong></td>
<td>Limit number of results (max 10000)</td>
<td>
[optional]
<tr>
<td><strong>search_after</strong></td>
<td><strong>str</strong></td>
<td>The sort value of the last item from the previous search, used to paginate. The results are sorted by _shard_doc when a PIT is used and by document id (_id) without a PIT. </td>
<td>
[optional]
<tr>
<td><strong>pit</strong></td>
<td><strong>str</strong></td>
<td>The pit id</td>
<td>
[optional]
<tr>
<td><strong>pretty</strong></td>
<td><strong>bool</strong></td>
<td>If true, the endpoint returns only the user metadata.</td>
<td>
[optional]
</tbody>
</table></div>


### Return type

[**QueryResponse**](QueryResponse.html)

### Authorization

[api_key](ObservatoryApi.html#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
<div class="wy-table-responsive"><table border="1" class="docutils">
<thead>
<tr>
<th>Status code</th>
<th>Description</th>
<th>Response headers</th>
</tr>
</thead>
<tbody>

<tr>
    <td><strong>200</strong></td>
    <td>Successfully return query results</td>
    <td> - </td>
</tr>
<tr>
    <td><strong>401</strong></td>
    <td>API key is missing or invalid</td>
    <td> * WWW_Authenticate -  <br> </td>
</tr>

</tbody>
</table></div>

## **query_subagg**
> QueryResponse query_subagg(agg, subagg)



### Example

* Api Key Authentication (api_key):
```python
import time
import package.client
from package.client.api import observatory_api
from package.client.model.query_response import QueryResponse
from pprint import pprint
# Defining the host is optional and defaults to https://ao-api.observatory.academy
# See configuration.py for a list of all supported configuration parameters.
configuration = package.client.Configuration(
    host = "https://ao-api.observatory.academy"
)

# The client must configure the authentication and authorization parameters
# in accordance with the API server security policy.
# Examples for each auth method are provided below, use the example that
# satisfies your auth use case.

# Configure API key authorization: api_key
configuration.api_key['api_key'] = 'YOUR_API_KEY'

# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['api_key'] = 'Bearer'

# Enter a context with an instance of the API client
with package.client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = observatory_api.ObservatoryApi(api_client)
    agg = "author" # str | The aggregate.
    subagg = "access-types" # str | The sub-aggregate.
    agg_id = [
        "agg_id_example",
    ] # [str] | Filter on aggregates with this id, if multiple values are given the results are filtered on whether there are aggregates with one of the given values.  (optional)
    subagg_id = [
        "subagg_id_example",
    ] # [str] | Filter on subaggregates with this id, if multiple values are given the results are filtered on whether there are subaggregates with one of the given values.  (optional)
    index_date = dateutil_parser('1970-01-01').date() # date | Index date, defaults to latest (optional)
    _from = dateutil_parser('1970-01-01').date() # date | Start year (included) (optional)
    to = dateutil_parser('1970-01-01').date() # date | End year (included) (optional)
    limit = 1 # int | Limit number of results (max 10000) (optional)
    search_after = "search_after_example" # str | The sort value of the last item from the previous search, used to paginate. The results are sorted by _shard_doc when a PIT is used and by document id (_id) without a PIT.  (optional)
    pit = "pit_example" # str | The pit id (optional)
    pretty = True # bool | If true, the endpoint returns only the user metadata. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.query_subagg(agg, subagg)
        pprint(api_response)
    except package.client.ApiException as e:
        print("Exception when calling ObservatoryApi->query_subagg: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.query_subagg(agg, subagg, agg_id=agg_id, subagg_id=subagg_id, index_date=index_date, _from=_from, to=to, limit=limit, search_after=search_after, pit=pit, pretty=pretty)
        pprint(api_response)
    except package.client.ApiException as e:
        print("Exception when calling ObservatoryApi->query_subagg: %s\n" % e)
```


### Parameters


<div class="wy-table-responsive"><table border="1" class="docutils">
<thead>
<tr>
<th>Name</th>
<th>Type</th>
<th>Description</th>
<th>Notes</th>
</tr>
</thead>
<tbody>



<tr>
<td><strong>agg</strong></td>
<td><strong>str</strong></td>
<td>The aggregate.</td>
<td></td>
</tr>

<tr>
<td><strong>subagg</strong></td>
<td><strong>str</strong></td>
<td>The sub-aggregate.</td>
<td></td>
</tr>





<tr>
<td><strong>agg_id</strong></td>
<td><strong>[str]</strong></td>
<td>Filter on aggregates with this id, if multiple values are given the results are filtered on whether there are aggregates with one of the given values. </td>
<td>
[optional]
<tr>
<td><strong>subagg_id</strong></td>
<td><strong>[str]</strong></td>
<td>Filter on subaggregates with this id, if multiple values are given the results are filtered on whether there are subaggregates with one of the given values. </td>
<td>
[optional]
<tr>
<td><strong>index_date</strong></td>
<td><strong>date</strong></td>
<td>Index date, defaults to latest</td>
<td>
[optional]
<tr>
<td><strong>_from</strong></td>
<td><strong>date</strong></td>
<td>Start year (included)</td>
<td>
[optional]
<tr>
<td><strong>to</strong></td>
<td><strong>date</strong></td>
<td>End year (included)</td>
<td>
[optional]
<tr>
<td><strong>limit</strong></td>
<td><strong>int</strong></td>
<td>Limit number of results (max 10000)</td>
<td>
[optional]
<tr>
<td><strong>search_after</strong></td>
<td><strong>str</strong></td>
<td>The sort value of the last item from the previous search, used to paginate. The results are sorted by _shard_doc when a PIT is used and by document id (_id) without a PIT. </td>
<td>
[optional]
<tr>
<td><strong>pit</strong></td>
<td><strong>str</strong></td>
<td>The pit id</td>
<td>
[optional]
<tr>
<td><strong>pretty</strong></td>
<td><strong>bool</strong></td>
<td>If true, the endpoint returns only the user metadata.</td>
<td>
[optional]
</tbody>
</table></div>


### Return type

[**QueryResponse**](QueryResponse.html)

### Authorization

[api_key](ObservatoryApi.html#api_key)

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details
<div class="wy-table-responsive"><table border="1" class="docutils">
<thead>
<tr>
<th>Status code</th>
<th>Description</th>
<th>Response headers</th>
</tr>
</thead>
<tbody>

<tr>
    <td><strong>200</strong></td>
    <td>Successfully return query results</td>
    <td> - </td>
</tr>
<tr>
    <td><strong>401</strong></td>
    <td>API key is missing or invalid</td>
    <td> * WWW_Authenticate -  <br> </td>
</tr>

</tbody>
</table></div>

