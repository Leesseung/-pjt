import { createRouter, createWebHistory } from 'vue-router'
import HomeView           from '@/views/HomePage/HomeView.vue'
import ProductsListView   from '@/views/Product/ProductsListView.vue'
import MyProductsView     from '@/views/Product/MyProductsView.vue'
import ChartView         from '@/views/Product/ChartView.vue'  // Add this line
import LogInView          from '@/views/HomePage/LogInView.vue'
import SignUpView         from '@/views/HomePage/SignUpView.vue'
import { useUserStore }   from '@/stores/userStore'
import LaterView from '@/views/Video/LaterView.vue'
import SearchView from '@/views/Video/SearchView.vue'
import DetailView from '@/views/Video/DetailView.vue'
import ChannelView from "@/views/Video/ChannelView.vue"
import BankSearchView from '@/views/Map/BankSearchView.vue'
import CommunityListView   from "@/views/Community/CommunityListView.vue"
import CommunityDetailView from "@/views/Community/CommunityDetailView.vue"
import CommunityCreateView from "@/views/Community/CommunityCreateView.vue"
import CommunityEditView   from "@/views/Community/CommunityEditView.vue"
import ProfileView from '@/views/Profile/ProfileView.vue'
import ProfileEdit from '@/views/Profile/ProfileEditView.vue'
import UserProfileView from '@/views/Profile/UserProfileView.vue'
import MyPostsListView from '@/views/Community/MyPostsListView.vue'

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/products',
    name: 'ProductsList',
    component: ProductsListView
  },
  {
    path: '/my-products',
    name: 'MyProducts',
    component: MyProductsView,
    meta: { requiresAuth: true }
  },
  {
    path: '/charts',
    name: 'Charts',
    component: ChartView,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'LogInView',
    component: LogInView
  },
  {
    path: '/signup',
    name: 'SignUpView',
    component: SignUpView
  },
  {
    path: "/search",
    name: "search",
    component: SearchView,
  },
  {
    path: "/later",
    name: "later",
    component: LaterView,
  },
  {
    path: "/videos/:videoId",
    name: "detail",
    component: DetailView,
  },
  {
    path: "/channels",
    name: "ChannelView",
    component: ChannelView,
  },
  {
    path: '/bank-search',
    name: 'BankSearch',
    component: BankSearchView
  },
  { 
    path: "/community",           
    name: "CommunityList",   
    component: CommunityListView 
  },
  { 
    path: "/community/create",    
    name: "CommunityCreate", 
    component: CommunityCreateView 
  },
  { 
    path: "/community/:id",       
    name: "CommunityDetail", 
    component: CommunityDetailView,
    props: true 
  },
  { 
    path: "/community/:id/edit",  
    name: "CommunityEdit",   
    component: CommunityEditView,
    props: true 
  },
  { 
    path: '/profile',      
    name: 'Profile',     
    component: ProfileView,
    meta: { requiresAuth: true }
  },
  { 
    path: '/profile/edit', 
    name: 'ProfileEdit', 
    component: ProfileEdit,
    meta: { requiresAuth: true }
  },
  { 
    path: '/users/:username', 
    name: 'UserProfile', 
    component: UserProfileView 
  },
  {
    path: '/community/mine',
    name: 'MyPosts',
    component: MyPostsListView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  if (to.meta.requiresAuth && !userStore.isLogin) {
    next({ name: 'LogInView' })
  } else {
    next()
  }
})

export default router