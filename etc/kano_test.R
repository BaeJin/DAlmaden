

rm(list=ls())
kano_raw <- read.csv("test_kano.csv",stringsAsFactors = F)

MIN_RADIOUS = 0.1
kano <- kano_raw %>% filter(group==2015)
kano <- kano %>% mutate(rPos=log(nPos)/sum(log(nPos)),
                            rNeg=log(nNeg)/sum(log(nNeg)),
                            rTot=(rPos+rNeg)/sum((rPos+rNeg)),
                            rCount=(rTot-min(rTot))/(max(rTot)-min(rTot)),
                            radious = MIN_RADIOUS + rCount*(1-MIN_RADIOUS),
                            
                            PosNeg = rPos / (rNeg + rPos),
                            rPositiveness = (PosNeg - min(PosNeg)) / (max(PosNeg) - min(PosNeg)),
                            theta = pi/4*rPositiveness,
                            x = cos(theta)*radious,
                            y = sin(theta)*radious)

ggplot(kano, aes(x=nPos, y=nNeg))+geom_point()
ggplot(kano, aes(x=x, y=y))+geom_point()
ggplot(kano, aes(x=log_rPos, y=log_rNeg))+geom_text(aes(label=label))
ggplot(kano, aes(x=tot_n, y=tot_r))+geom_point()




max_log_nPos = max(kano$log_nPos)
median_log_nPos = median(kano$log_nPos)
min_log_nPos = min(kano$log_nPos)
max_log_nNeg = max(kano$log_nNeg)
median_log_nNeg = median(kano$log_nNeg)
min_log_nNeg = min(kano$log_nNeg)



get_relativePositions <- function(x){
  if(x == median){
    return(0)
  }else{
    if(x<median){
      return((x-min)/(median-min)*0.5) 
    }else{
      return((x-median)/(max-median)*0.5 + 0.5)
    }
  }
}
kano <- kano %>% mutate(rPos=sapply(log_nPos,get_relativePosition,min_log_nPos,median_log_nPos,max_log_nPos),
                        rNeg=sapply(log_nNeg,get_relativePosition,min_log_nNeg,median_log_nNeg,max_log_nNeg))


ggplot(kano, aes(x=rPos,y=rNeg))+geom_point()
kano <- kano %>% mutate(tot = rPos+rNeg, ratio = rPos/rNeg)
ggplot(kano, aes(x=ratio,y=tot))+geom_point()

kano <- kano_raw %>% group_by(group) %>%
  mutate(nTot = nPos+nNeg,
         rTot = nTot/sum(nTot),
         rPos = nPos/sum(nPos), 
         rNeg = nNeg/sum(nNeg)) %>%
  arrange(group, desc(nTot)) %>%
  mutate(cTot = cumsum(nTot)/sum(nTot),
         rPos = rPos/(rPos+rNeg)) %>%
  mutate(tier_rTot = ifelse(rTot<=quantile(rTot,0.25)-1.5*(quantile(rTot,0.75)-quantile(rTot,0.25)),"T1",
                            ifelse(rTot<quantile(rTot,0.25),"T2",
                                   ifelse(rTot<quantile(rTot,0.5),"T3",
                                          ifelse(rTot<quantile(rTot,0.75),"T4",
                                                 ifelse(rTot<quantile(rTot,0.75)+1.5*(quantile(rTot,0.75)-quantile(rTot,0.25)),"T5","T6"))))),
         tier_rPos = ifelse(rPos<=quantile(rPos,0.25)-1.5*(quantile(rPos,0.75)-quantile(rPos,0.25)),"T1",
                            ifelse(rPos<quantile(rPos,0.25),"T2",
                                   ifelse(rPos<quantile(rPos,0.5),"T3",
                                          ifelse(rPos<quantile(rPos,0.75),"T4",
                                                 ifelse(rPos<quantile(rPos,0.75)+1.5*(quantile(rPos,0.75)-quantile(rPos,0.25)),"T5","T6")))))) %>%
  group_by(group,tier_rTot) %>%
  mutate(tier_rTot_max = max(rTot),
         tier_rTot_min = min(rTot),
         tier_rTot_gap = max(rTot)-min(rTot)) %>%
  ungroup() %>%
  group_by(group, tier_rPos) %>%
  mutate(tier_rPos_max = max(rPos),
         tier_rPos_min = min(rPos),
         tier_rPos_gap = max(rPos)-min(rPos)) %>%
  mutate(radius = ifelse(tier_rTot=="T1", 1-0.1,
                         ifelse(tier_rTot=="T2", 1+(rTot-tier_rTot_min)/tier_rTot_gap,
                                ifelse(tier_rTot=="T3", 2+(rTot-tier_rTot_min)/tier_rTot_gap,
                                       ifelse(tier_rTot=="T4", 3+(rTot-tier_rTot_min)/tier_rTot_gap,
                                              ifelse(tier_rTot=="T5", 4+(rTot-tier_rTot_min)/tier_rTot_gap,
                                                     5+0.1))))),
         radian = ifelse(tier_rPos=="T1", 0,
                         ifelse(tier_rPos=="T2", 0+(rPos-tier_rPos_min)*pi/8/tier_rPos_gap,
                                ifelse(tier_rPos=="T3", 1*pi/8+(rPos-tier_rPos_min)*pi/8/tier_rPos_gap,
                                       ifelse(tier_rPos=="T4", 2*pi/8+(rPos-tier_rPos_min)*pi/8/tier_rPos_gap,
                                              ifelse(tier_rPos=="T5", 3*pi/8+(rPos-tier_rPos_min)*pi/8/tier_rPos_gap,
                                                     pi/2))))),
         loc_x = cos(radian)*radius,
         loc_y = sin(radian)*radius
  )

#dummy circle files
n=100
lines = data.frame(d=rep(seq(0,n)/n,5),
                   r=sort(rep(1:5,n+1)))%>%
  mutate(x=r*cos(d*pi/2),
         y=r*sin(d*pi/2))

seg_lines_1 = lines %>% filter(r==2) 
seg_lines_2 = lines %>% filter(r>=2&d==3/4) %>% rbind(data.frame(d=3/4,
                                                                 r=5.5)%>%
                                                        mutate(x=r*cos(d*pi/2),
                                                               y=r*sin(d*pi/2)))
seg_lines_3 = lines %>% filter(r>=2&d==1/4) %>% rbind(data.frame(d=1/4,
                                                                 r=5.5)%>%
                                                        mutate(x=r*cos(d*pi/2),
                                                               y=r*sin(d*pi/2)))
tags = data.frame(tags=c("In-different","Attractive","One-dimensional","Must-be"),
                  x = c(0.5,1,4,5),
                  y = c(0.5,5.5,4,1))

vis_base = ggplot()+
  geom_line(data=lines, aes(x=x,y=y,group=r), col="grey")+
  geom_abline(slope=c(tan(0*pi/2),tan(0.25*pi/2),tan(0.5*pi/2),tan(0.75*pi/2),tan(1*pi/2)),col="grey")+
  geom_line(data=seg_lines_1,aes(x=x, y=y),size=2,col="grey")+
  geom_line(data=seg_lines_2,aes(x=x, y=y),size=2,col="grey")+
  geom_line(data=seg_lines_3,aes(x=x, y=y),size=2,col="grey")+
  geom_text(data=tags,aes(x=x,y=y,label=tags))+
  theme_classic()+
  xlim(-0.1,5.5)+ylim(-0.1,5.5)

vis_base +
  #geom_point(files=kano%>%filter(group%in%c(2018)), aes(x=loc_x, y=loc_y, col=label)) +
  #geom_path(files=kano%>%filter(group%in%c(2018)), aes(x=loc_x, y=loc_y, group=label, col=label),
  #          alpha=0.5,arrow=arrow(angle=15, type="closed"))+
  geom_text(data=kano%>%filter(group==2015),aes(x=loc_x, y=loc_y,label=label, col=label)
            #position=position_jitter(height=0.2)
  )+
  theme(legend.position = "none")
