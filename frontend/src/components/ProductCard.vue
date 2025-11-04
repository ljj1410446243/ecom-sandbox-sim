<script setup lang="ts">
const props = defineProps<{
  product: {
    id:string
    name:string
    product_code:string
    category:string
    base_cost:string
  }
}>()
</script>

<template>
<!--  <el-card class="product-card" :body-style="{ padding: '20px' }">-->
<!--&lt;!&ndash;    <el-image :src="props.product.image" fit="cover" class="product-image" />&ndash;&gt;-->
<!--    <div class="product-info">-->
<!--      <div class="product-title">{{ props.product.name }}</div>-->
<!--      <div class="product-code">{{ props.product.product_code }}</div>-->
<!--      <el-tag class="product-category">{{ props.product.category }}</el-tag>-->
<!--      <div class="product-price">￥{{ props.product.base_cost }}</div>-->
<!--    </div>-->
<!--  </el-card>-->
  <div class="container">
	<!-- code here -->
	<div class="card">
		<div class="card-img">
			<img src="https://assets.codepen.io/285131/uslmOwQpdRRUwr6AmBP6JdzeHjS.jpg" />
		</div>
		<div class="card-body">
			<h2 class="card-title">
				{{ props.product.name }}
        <el-tag class="product-category">{{ props.product.category }}</el-tag>
			</h2>
			<p class="card-intro">
				￥{{ props.product.base_cost }}
			</p>
		</div>
	</div>
</div>
</template>

<style lang="less" scoped>

*, *:after, *:before {
	box-sizing: border-box;
}

body {
	font-family: "Inter", sans-serif;
	background-color: #f2f5f7;
}

.card {
	display: flex;
	flex-direction: column;
	flex-basis: 300px;
	flex-shrink: 0;
	flex-grow: 0;
	max-width: 100%;
  height: 100%;
	background-color: #FFF;
	box-shadow: 0 5px 10px 0 rgba(#000, .15);
	border-radius: 10px;
	overflow: hidden;
	margin: 1rem;
}

.card-img {
	padding-bottom: 45%;
	position: relative;
	img {
		position: absolute;
		width: 100%;
	}
}

.card-body {
	padding: 1.5rem;
}

.card-title {
	font-size: 1.25rem;
	line-height: 1.33;
	font-weight: 700;
}

.card-intro {
	margin-top: .75rem;
	line-height: 1.5;

}


@keyframes shine {
	to {
		background-position: right -40px top 0;
	}
}

.container {
  margin-bottom: 50px;
	width: 100%;
  height: 250px;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-wrap: wrap;
}
</style>
