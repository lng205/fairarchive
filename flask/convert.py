import re

# Example text
text = """
{% import "macros.html" as macros %}

{% extends "base.html" %}

{% block title %}{{ post['title'] }} - 集市档案{% endblock %}

{% block content %}
<div class="container py-4 border-bottom">
  <!-- author -->
  <div class="container ps-0 d-flex text-muted">
    <img src="{{ post['headimgurl'] }}" alt="headimg" class="rounded-circle" style="width: 21px; height: 21px;">
    <small>&nbsp;{{ post['nickname'] }}&nbsp;</small><small data-timestamp="{{ post['p_time'] }}"></small>
  </div>

  <h3 class="title">{{ post['title'] }}</h3>
  <p>{{ post['content'] }}</p>

  <!-- images -->
  <div id="carouselExampleIndicators" class="carousel slide">
    <ol class="carousel-indicators">
      {% for pic in post['img_paths'] %}
      <button type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide-to="{{ loop.index0 }}"
      {% if loop.first %}class="active" aria-current="true"{% endif %}
      aria-label="Slide {{ loop.index }}"></button>
      {% endfor %}
    </ol>
    <div class="carousel-inner">
      {% for pic in post['img_paths'] %}
      <div class="carousel-item {% if loop.first %}active{% endif %}">
        <img src="https://b1.cdn.zanao.com/{{ pic }}@!common" class="d-block" alt="post pic">
      </div>
      {% endfor %}
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="prev">
      <span class="carousel-control-prev-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleIndicators" data-bs-slide="next">
      <span class="carousel-control-next-icon" aria-hidden="true"></span>
      <span class="visually-hidden">Next</span>
    </button>
  </div>
</div>
<div class="container mt-5 px-0">
  <!-- Define a macro for displaying a single comment and its nested replies -->
  {% macro display_comment(comment) %}
  <div class="card mb-2">
    <div class="card-body">
      <div class="d-flex gap-2">
        <img src="{{ comment['headimgurl'] }}" alt="Profile Picture" class="rounded-circle"
          style="width: 48px; height: 48px;">
        <div>
          <div class="d-flex gap-2">
            <span>{{ comment['nickname'] }}</span>
            <span class="text-muted" data-timestamp="{{ comment['post_time'] }}"></span>

            <!-- like num -->
            <span class="text-danger">
              <i class="bi-hand-thumbs-up-fill"></i>
              <span class="stats">{{ comment['like_num'] }}</span>
            </span>
          </div>
          <p class="mb-1">
            {% if comment['reply_to'] %}
            <span class="text-muted">回复@{{ comment['reply_to'] }}：</span>{% endif %}{{ comment['content'] }}
          </p>
        </div>
      </div>
      <!-- Recursively display replies, if any -->
      {% if comment['replies'] %}
      <div class="ms-4">
        {% for reply in comment['replies'] %}
        {{ display_comment(reply) }}
        {% endfor %}
      </div>
      {% endif %}
    </div>
  </div>
  {% endmacro %}

  <!-- Use the macro to display each root comment and its replies -->
  {% for comment in comments %}
  {{ display_comment(comment) }}
  {% endfor %}
</div>
{% endblock %}


"""

# Pattern to find and replace
pattern = r"(\w*)\['(\w*?)'\]"
replacement = r"\1.\2"

# Replacement operation
replaced_text = re.sub(pattern, replacement, text)

print(replaced_text)
