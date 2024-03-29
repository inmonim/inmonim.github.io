
home에서 포스팅의 미리보기 이미지는 다음 절차를 따르자!

아래의 코드를 home.html의 48 line에 붙여넣자!

{% if post.image %}
  {% assign src = post.image.path | default: post.image %}
  {% unless src contains '//' %}
    {% assign src = post.img_path | append: '/' | append: src | replace: '//', '/' %}
  {% endunless %}

  {% assign alt = post.image.alt | xml_escape | default: 'Preview Image' %}

  {% assign lqip = null %}

  {% if post.image.lqip %}
    {% capture lqip %}lqip="{{ post.image.lqip }}"{% endcapture %}
  {% endif %}

  <div class="col-md-5">
    <img src="{{ src }}" alt="{{ alt }}" {{ lqip }}>
  </div>

  {% assign card_body_col = '7' %}
{% endif %}