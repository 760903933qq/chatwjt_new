<script setup>
import Header from '@/components/Header.vue'
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header style="height: 20%; padding: 0">
        <Header />
      </el-header>
      <el-main style="height: 80%; padding: 0">
        <RouterView />
      </el-main>
    </el-container>
  </div>
</template>

<style scoped></style>
