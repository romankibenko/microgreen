<script setup lang="ts">
import { ref } from 'vue'

import AppHeader from '@/components/AppHeader.vue'
import CartDrawer from '@/components/cart/CartDrawer.vue'
import ProductCatalog from '@/components/catalog/ProductCatalog.vue'
import CheckoutDialog from '@/components/checkout/CheckoutDialog.vue'
import HeroSection from '@/components/HeroSection.vue'
import type { Order, Product } from '@/api/types'
import { useCartStore } from '@/stores/cart'

const cart = useCartStore()

const drawerOpen = ref(false)
const checkoutOpen = ref(false)
const snackbar = ref(false)
const snackbarText = ref('')

function handleAdd(product: Product): void {
  cart.add(product)
  snackbarText.value = `«${product.name}» в корзине`
  snackbar.value = true
}

function startCheckout(): void {
  drawerOpen.value = false
  checkoutOpen.value = true
}

function onOrderSuccess(order: Order): void {
  snackbarText.value = `Заказ №${order.id} принят! Скоро позвоним 🌱`
  snackbar.value = true
}

function scrollToCatalog(): void {
  document.getElementById('catalog')?.scrollIntoView({ behavior: 'smooth' })
}
</script>

<template>
  <v-app>
    <AppHeader :cart-count="cart.count" @open-cart="drawerOpen = true" />

    <v-main>
      <HeroSection @browse="scrollToCatalog" />
      <ProductCatalog @add="handleAdd" />
    </v-main>

    <CartDrawer v-model="drawerOpen" @checkout="startCheckout" />
    <CheckoutDialog v-model="checkoutOpen" @success="onOrderSuccess" />

    <v-snackbar v-model="snackbar" color="primary" timeout="2600" location="bottom">
      {{ snackbarText }}
    </v-snackbar>
  </v-app>
</template>
