# QueryResponse

## Properties
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
    <td><strong>version</strong></td>
    <td><strong>str</strong></td>
    <td>The API version</td>
    <td>[optional] </td>
</tr>
<tr>
    <td><strong>index</strong></td>
    <td><strong>str</strong></td>
    <td>The full name of the elasticsearch index that is searched</td>
    <td>[optional] </td>
</tr>
<tr>
    <td><strong>pit</strong></td>
    <td><strong>str</strong></td>
    <td>The most recent Point In Time id of the index that is searched, each search request can return a different id; thus always use the most recently received id for the next search request. </td>
    <td>[optional] </td>
</tr>
<tr>
    <td><strong>search_after</strong></td>
    <td><strong>str</strong></td>
    <td>The sort value of the last item from the previous search, used to paginate. The results are sorted by _shard_doc when a PIT is used and by document id (_id) without a PIT. </td>
    <td>[optional] </td>
</tr>
<tr>
    <td><strong>returned_hits</strong></td>
    <td><strong>int</strong></td>
    <td>The number of returned hits (can be less than total_hits if a limit is set)</td>
    <td>[optional] </td>
</tr>
<tr>
    <td><strong>total_hits</strong></td>
    <td><strong>int</strong></td>
    <td>The number of total hits</td>
    <td>[optional] </td>
</tr>
<tr>
    <td><strong>schema</strong></td>
    <td><strong>bool, date, datetime, dict, float, int, list, str, none_type</strong></td>
    <td>The schema for an individual hit</td>
    <td>[optional] </td>
</tr>
<tr>
    <td><strong>results</strong></td>
    <td><strong>[bool, date, datetime, dict, float, int, list, str, none_type]</strong></td>
    <td>A list of the actual results (one dictionary per hit)</td>
    <td>[optional] </td>
</tr>


</tbody>
</table></div>

