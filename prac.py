   <!-- <div class="container">
    {% include 'partials/messages.html' %}

    {% if income.count %}

    <div class="row">
      <div class="col-md-8"></div>
      <div class="col-md-4">

        <div class="form-group">
          <input type="text" class="form-control" id="searchField" placeholder="Search">
        </div>
      </div>
     </div>
<div class="app-table">

  <table class="table table-stripped table-hover">
    <thead>
      <tr>
        <th>Amount ({{currency}})</th>
        <th>Source</th>
        <th>Description</th>
        <th>Date</th>
        <th></th>
      </tr>
    </thead>

    <tbody>
      {% for income in page_obj%}
      <tr>
        <td>{{income.amount}}</td>
        <td>{{income.source}}</td>
        <td>{{income.description}}</td>
        <td>{{income.date}}</td>

        <td>
          <a
            href="{% url 'income-edit' income.id  %}"
            class="btn btn-secondary btn-sm"
            >Edit</a
          >
        </td>
      </tr>

      {% endfor %}
    </tbody>
  </table>
</div>

<p class="no-results" style="display: none;">No results </p>
    <div class="table-output">


      <table class="table table-stripped table-hover">
        <thead>
          <tr>
            <th>Amount ({{currency}})</th>
            <th>Source</th>
            <th>Description</th>
            <th>Date</th>
            <th></th>
          </tr>
        </thead>

        <tbody  class="table-body">


        </tbody>
      </table>
    </div>




    <div class="pagination-container">
    <div class="">
      Showing page {{page_obj.number}} of {{ page_obj.paginator.num_pages }}
    </div>
    <ul class="pagination align-right float-right mr-auto">
      {% if page_obj.has_previous %}
      <li {% if page_obj.number == 1 %} class="page-item active" {% endif %}><a class="page-link" href="?page=1">&laquo; 1</a></li>
      <li class="page-item"> <a class="page-link" href="?page={{ page_obj.previous_page_number }}">Previous</a></li>
      {% endif %}

      {% if page_obj.has_next %}
      <li class="page-item"> <a class="page-link" href="?page={{ page_obj.next_page_number }}">Next</a></li>
      <li class="page-item"> <a class="page-link" href="?page={{ page_obj.paginator.num_pages }}">{{ page_obj.paginator.num_pages}} &raquo;</a></li>
      {% endif %}


      </ul>
    {% endif %}
  </div>
</div> -->