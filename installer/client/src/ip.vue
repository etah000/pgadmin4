<template>
  <div>
    <ul class="ipAdress">
      <!--eslint-disable-next-line-->
      <li v-for="(item,index) in ipAdress" >
        <!--eslint-disable-next-line-->
        <input type="text" @input="checkIpVal(item,index)" @keyup="turnIpPOS(item,index,$event)" v-model:value="item.value" ref="ipInput" @blur="setDefaultVal(item)" @change="handleChange"/>
        <div v-if="index!=3"></div>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "ip",
  props: ['index','ip'],
  /*  model: {
      prop: 'ip',  // props接受的变量名称
      event: 'change'  //定义一个方法
    },*/
  data(){
    return {
      ipAdress: [{
        value: this.ip.split('.')[0]
      }, {
        value: this.ip.split('.')[1]
      }, {
        value: this.ip.split('.')[2]
      }, {
        value: this.ip.split('.')[3]
      }]
    }
  },
  methods: {
    checkIpVal(item, index) {
      //确保每个值都处于0-255
      let val = item.value;
      //当输入的是空格时，值赋为空
      val = val.trim();
      val = parseInt(val, 10);
      if (isNaN(val)) {
        val = ''
      } else {
        val = val < 0 ? 0 : val;
        val = val > 255 ? 255 : val;
      }
      item.value = val;
    },
    turnIpPOS(item, index, event) {
      let self = this;
      let e = event || window.event;
      // console.log(index);
      //删除键把当前数据删除完毕后会跳转到前一个input，左一不做任何处理
      if (e.keyCode == 8) {
        let val = item.value;
        if (index != 0 && val==''){
          self.$refs.ipInput[index - 1].focus();
        }
      }
      //右箭头、回车键、空格键、冒号均向右跳转，右一不做任何措施
      if (e.keyCode == 39 || e.keyCode == 13 || e.keyCode == 32 || e.keyCode == 190 || e.keyCode == 110) {
        if (index != 3) {
          self.$refs.ipInput[index + 1].focus();
        }
      }
    },
    setDefaultVal(item) {
      //当input失去焦点，而ip没有赋值时，会自动赋值为0
      let val = item.value;
      if (val == '') {
        item.value = '0';
      }
    },
    handleChange(){
      this.ip = this.ipAdress.map(e=> {return e.value}).join('.')
      this.$emit('change',this.index,this.ip,this.port);
    }
  }
}
</script>

<style scoped>
.ipAdress {
  display: flex;
  align-items: center;
  border: 1px solid #DCDFE6;
  width: 200px;
  margin-right: 10px;
  padding: 0;
}

.ipAdress li {
  position: relative;
  height: 30px;
  margin: 0;
  list-style: none;
}

ul[class="ipAdress"] input[type="text"] {
  border: none;
  width: 100%;
  height: 30px;
  text-align: center;
  background: transparent;
  color: #000;
}

.ipAdress li div {
  position: absolute;
  bottom: 2px;
  right: 0;
  border-radius: 50%;
  background: #0190FE;
  width: 2px;
  height: 2px;
}

/*只需要3个div*/
.ipAdress li:last-child div {
  display: none;
}

/*取消掉默认的input focus状态*/
.ipAdress input:focus {
  outline: none;
}
</style>
