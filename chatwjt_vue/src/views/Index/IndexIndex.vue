<template>
  <!-- 聊天列表 -->
  <el-drawer
    v-model="drawer"
    direction="ltr"
    :show-close="false"
    size="200px"
    :with-header="false"
  >
    <template #default>
      <div class="drawer-header">
        <el-button type="success" text @click="newLabel">新建聊天</el-button>
        <el-button
          type="danger"
          @click="delLabel"
          :icon="Delete"
          text
        ></el-button>
      </div>
      <el-menu
        :default-active="`${activeIndex}`"
        :router="false"
        style="border: none"
        @select="handleSelect"
      >
        <el-menu-item
          v-for="(item, i) in labels"
          :key="item"
          :index="i.toString()"
          >{{ item }}</el-menu-item
        >
      </el-menu>
    </template>
  </el-drawer>
  <!-- 新建聊天 -->
  <el-dialog v-model="dialogVisible" title="新建聊天" width="70%">
    <el-input
      placeholder="请输入聊天名称"
      v-model="chatName"
      :maxlength="10"
    ></el-input>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmNew">确认</el-button>
      </span>
    </template>
  </el-dialog>

  <!-- 聊天框 -->
  <el-row justify="center">
    <el-col>
      <el-card
        style="min-height: 88vh"
        :body-style="{
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: '0',
        }"
      >
        <template #header>
          <div class="card-header" style="height: 5px">
            <span>{{ label }}</span>
            <el-button
              type="primary"
              style="margin-left: 16px"
              @click="drawer = true"
            >
              聊天列表
            </el-button>
          </div>
        </template>
        <div
          style="
            height: calc(88vh - 80px);
            overflow-y: auto;
            overflow-x: hidden;
          "
          ref="messagesEnd"
        >
          <div v-for="(item, index) in messages" :key="index">
            <el-row
              align="middle"
              class="userMessage message"
              v-if="item.sender === 0"
            >
              <el-col
                :span="1"
                :offset="1"
                style="
                  display: flex;
                  justify-content: center;
                  margin-left: 10px;
                "
              >
                <img
                  src="@/assets/images/小狗.svg"
                  alt=""
                  style="width: 30px"
                />
              </el-col>
              <el-col :span="19" :offset="1">
                <!-- 用户消息 -->
                <div style="padding: 3px">{{ item.content }}</div>
              </el-col>
              <el-col
                :span="1"
                :offset="1"
                style="display: flex; justify-content: end"
              >
                <el-button
                  v-if="!item.star"
                  type="primary"
                  :icon="List"
                  circle
                  text
                  @click="star(index)"
                />
                <el-button
                  v-else
                  type="danger"
                  :icon="List"
                  circle
                  text
                  @click="star(index)"
                />
              </el-col>
            </el-row>
            <el-row align="middle" class="aiMessage message" v-else>
              <el-col
                :span="1"
                style="
                  display: flex;
                  justify-content: center;
                  margin-left: 10px;
                "
              >
                <img
                  src="@/assets/images/青蛙.svg"
                  alt=""
                  style="width: 30px"
                />
              </el-col>
              <el-col :span="19" :offset="1" style="overflow-x: auto">
                <!-- AI回复 -->
                <div
                  v-html="marked.parse(item.content)"
                  style="padding: 3px"
                ></div>
              </el-col>
              <el-col
                :span="1"
                :offset="1"
                style="display: flex; justify-content: end"
              >
                <el-button
                  v-if="!item.star"
                  type="primary"
                  :icon="List"
                  circle
                  text
                  @click="star(index)"
                />
                <el-button
                  v-else
                  type="danger"
                  :icon="List"
                  circle
                  text
                  @click="star(index)"
                />
              </el-col>
            </el-row>
          </div>
        </div>
        <form id="chat-form" @submit.prevent="sendMessage">
          <div class="input">
            <el-input
              placeholder="请输入内容"
              v-model="message"
              style="height: 100%"
              size="large"
              :input-style="{
                height: '100%',
                borderRadius: '0',
              }"
              class="my-input"
              :disabled="sendbtn"
            />
            <div class="inputbutton">
              <el-button
                class="el-button el-button--primary"
                style="height: 100%"
                :disabled="sendbtn"
                @click="sendMessage"
              >
                发送
              </el-button>
            </div>
          </div>
        </form>
      </el-card>
    </el-col>
  </el-row>
</template>

<style>
.input {
  display: flex;
  justify-content: space-between;
  height: 40px;
}

.message {
  min-height: 50px;
}

.userMessage {
  background-color: #f5f5f5;
}

.aiMessage {
  background-color: #e6f7ff;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 14px;
  border-bottom: 1px solid #826858;
}
.my-input .el-input__inner {
  color: black;
  font-size: 16px;
}
</style>

<script setup>
import { ref, computed, nextTick } from "vue";
import { Delete, List } from "@element-plus/icons-vue";
import { useWebSocket } from "@vueuse/core";
import { useUserStore } from "@/stores/userInfo";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
// 显示markdown格式
import { marked } from "marked";
import { mangle } from "marked-mangle";
import { gfmHeadingId } from "marked-gfm-heading-id";
import { markedHighlight } from "marked-highlight";
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";
import { rightAPI } from "@/apis/chat";

const router = useRouter();
async function getRight() {
  const res = await rightAPI();
  if (res.code === 200) {
    ElMessage({
      message: "登陆成功",
      type: "success",
    });

    return;
  } else if (res.code === 202) {
    router.push("/user/login");
  } else {
    router.push("/user/");
  }
}

getRight().then(() => {
  if (localStorage.getItem("notification") === "confirmed") {
    return;
  } else {
    ElMessageBox.alert(
      "\t\t\t\t\t我们进行了一个大的版本更新, 优化了您的体验, 但不幸的是您的聊天数据并没有迁移到新的版本, 我们决定继续运行旧版本直到6月7日,因此您可以选择去旧版本处理您的数据, 您可以复制以下网址跳转到旧版本(请注意这条消息只会弹出一次, 因此请务必保存好旧版本的网址):\n\nhttps://www.chatwjt.com:444",
      "通知",
      {
        confirmButtonText: "OK",
        callback: () => {
          localStorage.setItem("notification", "confirmed");
        },
      }
    );
  }
});

const options = {
  prefix: "my-prefix-",
};
const originalWarn = console.warn;
console.warn = function (msg) {
  if (msg) {
    if (typeof msg === "string") {
      if (!msg.includes("sanitize and sanitizer parameters are deprecated")) {
        originalWarn.apply(console, arguments);
      }
    }
  }
};
marked.use(
  markedHighlight({
    langPrefix: "hljs language-",
    highlight(code, lang) {
      const language = hljs.getLanguage(lang) ? lang : "plaintext";
      return hljs.highlight(code, { language }).value;
    },
  })
);
marked.use(gfmHeadingId(options));
marked.use(mangle());
marked.use({
  sanitize: true,
});
const labels = ref([]);
const messages = ref([]);
const message = ref("");
const drawer = ref(false);
const star = (index) => {
  messages.value[index].star = !messages.value[index].star;
};
const id = ref(-1);
const userStore = useUserStore();
const messagesEnd = ref(null);

function scrollToBottom() {
  messagesEnd.value.scrollTop = messagesEnd.value.scrollHeight;
}
const token = userStore.userInfo.token;
const { send, data } = useWebSocket("wss://www.chatwjt.com:443/ws/chat", {
  // const { send, data } = useWebSocket("ws://127.0.0.1:8000/ws/chat", {
  onMessage: () => {
    const message = data.value;
    if (message === "pong") {
      return;
    } else {
      const messageObj = JSON.parse(message);
      if (messageObj.status === "chat_label") {
        labels.value = messageObj.chat_label;
        if (labels.value.length > 0) {
          handleSelect(0);
        }
        return;
      } else if (messageObj.status === "del_success") {
        labels.value.splice(labels.value.indexOf(label.value), 1);
        if (labels.value.length > 0) {
          handleSelect(0);
        } else {
          messages.value = [];
          label.value = "";
        }
        return;
      } else if (messageObj.status === "add_success") {
        handleSelect(labels.value.length - 1);
        return;
      } else {
        if (id.value !== messageObj.id) {
          id.value = messageObj.id;
          messages.value.push(messageObj);
          nextTick(() => {
            scrollToBottom();
          });
        } else {
          if (messageObj) {
            messages.value[messages.value.length - 1].content +=
              messageObj.content;
            nextTick(() => {
              scrollToBottom();
            });
          }
        }
      }
    }
  },
  onConnected: () => {
    send("token " + token);
    send("getchatlableshc93h4uh2g4i9a");
  },
  onDisconnected: () => {},
  heartbeat: {
    message: "ping",
    interval: 6000,
    pongTimeout: 6000,
  },
});
const starIds = computed(() => {
  return messages.value
    .filter((message) => message.star)
    .map((message) => message.id);
});
const label = ref("");
function setAllStarFalse() {
  messages.value.forEach((message) => {
    message.star = false;
  });
}
const sendMessage = () => {
  if (message.value === "") {
    return;
  } else {
    const json = JSON.stringify({
      content: message.value,
      star: starIds.value,
    });
    send(json);
    setAllStarFalse();
    messages.value.push({
      sender: 0,
      content: message.value,
      star: true,
      label: label.value,
      id: messages.value.length + 1,
    });
    message.value = "";
    nextTick(() => {
      scrollToBottom();
    });
  }
};

// 自动滚动到底部

// 聊天列表功能区
let activeIndex = ref(0);
// 切换列表
const handleSelect = (key) => {
  label.value = labels.value[key];
  activeIndex.value = key;
  messages.value = [];
  send("chatlistjoidwaj98y4h0h1c4" + " " + label.value);
};
const dialogVisible = ref(false);
const chatName = ref("");
const newLabel = () => {
  dialogVisible.value = true;
};
const confirmNew = () => {
  if (labels.value.includes(chatName.value)) {
    dialogVisible.value = false;
    chatName.value = "";
  } else {
    dialogVisible.value = false;
    labels.value.push(chatName.value);
    send("addLabel0j13e09ujv09ujdv0s8ujv12-" + " " + chatName.value);
    chatName.value = "";
  }
};
const delLabel = () => {
  send("delLabel0dha0shd10nv09isad-34" + " " + label.value);
};

// 发送按钮是否激活
const sendbtn = computed(() => {
  return labels.value.length <= 0; // 判断列表是否有值
});
</script>
