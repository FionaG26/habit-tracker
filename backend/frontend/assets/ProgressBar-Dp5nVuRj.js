import{_ as l,c as t,o as s,a,e as i,t as r,n}from"./index-Dx0mkLL9.js";const d={data(){return{milestoneMessage:""}},computed:{completedHabits(){return this.$store.state.habits.filter(o=>o.completed).length},totalHabits(){return this.$store.state.habits.length},progressPercentage(){return this.completedHabits/this.totalHabits*100||0},milestoneAchieved(){return this.completedHabits===5?(this.milestoneMessage="5 Habits Completed!",!0):this.completedHabits===10?(this.milestoneMessage="10-Day Streak!",!0):!1}}},m={class:"progress-container"},h={class:"mb-2"},p={class:"progress-bar-container"},_={key:0,class:"celebration"},b={key:1,class:"milestone"};function g(o,u,f,H,c,e){return s(),t("div",m,[a("p",h,"Habits Completed: "+r(e.completedHabits)+"/"+r(e.totalHabits),1),a("div",p,[a("div",{class:"progress-bar",style:n({width:e.progressPercentage+"%"})},null,4)]),e.progressPercentage===100?(s(),t("div",_," 🎉 Great job! All habits completed! 🎉 ")):i("",!0),e.milestoneAchieved?(s(),t("div",b," 🏆 Achievement Unlocked: "+r(c.milestoneMessage),1)):i("",!0)])}const k=l(d,[["render",g],["__scopeId","data-v-0317246c"]]);export{k as default};
