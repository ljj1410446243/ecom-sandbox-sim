
<template>
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
    <div class="card-footer">
      <!-- 购物车操作区域 -->
      <div class="cart-actions">
        <div class="quantity-selector">
          <el-input-number
              v-model="quantity"
              :min="1"
              :max="999"
              size="small"
              controls-position="right"
          />
        </div>
        <el-button
            type="primary"
            size="small"
            @click="addToInventory"
            class="add-to-cart-btn"
        >
            购入仓库
        </el-button>
      </div>
    </div>
	</div>
</div>
</template>
<script setup lang="ts">
import {setInventory} from "../api";

const props = defineProps<{
  product: {
    id:string
    name:string
    product_code:string
    category:string
    base_cost:string
  }
}>()

const addToInventory = () => {
  setInventory()
}
</script>

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
  margin: 1.5rem;
  height: 25%;
}
.card-footer {
  margin: 1.5rem;
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
  height: 500px;
	display: flex;
	align-items: center;
	justify-content: center;
	flex-wrap: wrap;
}
</style>
