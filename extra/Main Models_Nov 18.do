
***Panel data preparation

format date %tw
xtset platform_id date

//Optional to fill in the gaps in time series data
 tsfill
 
 //set of controls worked for the IV for main effect
 log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_Platform_Age_lag reddit_subscribers lgithub_n_issues_lag i.month
 
 
 //Main results table

asdoc xtscc log_hashrate  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag log_Platform_Age_lag log_hashrate_lag i.month, fe replace save(XTSCC_Main Results) nest cnames(log_Hashrate)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_n_proposals c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_number_proposals)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_N_topics  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_N_topics_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag  log_Platform_Age_lag i.month, fe nest cnames(log_N_topics)  drop(i.month) dec(3) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)

asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_reddit_subscribers_lag   log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_hashrate_lag log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_reddit_subscribers_lag  log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag  log_reddit_subscribers_lag log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
 asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag   log_N_topics_lag log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag  log_reddit_subscribers_lag log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)

 //Plot the nolinear relationship
 margins, at(log_Block_invHHI3_lag=(0(0.5)5))
 marginsplot, title("Predictive margins with 95% CIs") ///
ylabel(15(1)22) xlabel(0(0.5)5) ///
xtitle("log(Operational Decentralization)_lag") ytitle("log(Market Capitalization)")

 
margins, at(log_Commit_invHHI_lag=(0(0.5)5))
marginsplot, title("Predictive margins with 95% CIs") ///
ylabel(15(1)22) xlabel(0(0.5)5) ///
xtitle("log(Development Decentralization)_lag") ytitle("log(Market Capitalization)")

//Robustness check - address reverse causality with lagged two terms decentralization and lagged one term mediators

asdoc xtscc log_MC c.log_Block_invHHI3_lag2##c.log_Block_invHHI3_lag2 c.log_Commit_invHHI_lag2##c.log_Commit_invHHI_lag2 log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_reddit_subscribers_lag   log_Platform_Age_lag i.month, fe replace save(XTSCC_Robustness_Lagged) cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag2##c.log_Block_invHHI3_lag2 c.log_Commit_invHHI_lag2##c.log_Commit_invHHI_lag2 log_hashrate_lag log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_reddit_subscribers_lag  log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag2##c.log_Block_invHHI3_lag2 c.log_Commit_invHHI_lag2##c.log_Commit_invHHI_lag2 log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag  log_reddit_subscribers_lag log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
 asdoc xtscc log_MC c.log_Block_invHHI3_lag2##c.log_Block_invHHI3_lag2 c.log_Commit_invHHI_lag2##c.log_Commit_invHHI_lag2   log_N_topics_lag log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag  log_reddit_subscribers_lag log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)




 
 asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_Platform_Age_lag   i.month, fe replace save(XTSCC_Mediation Effect-7d_lag) nest cnames(log_MC-Total Effect)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_n_proposals c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_number_proposals)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag log_reddit_comments_lag lreddit_posts_lag log_Platform_Age_lag i.month, fe nest cnames(log_MC-Direct Effect) dec(2)  drop(i.month) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
 
 
 //Original main models

asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe replace save(XTSCC_Mediation Effect-7d_lag) nest cnames(log_MC-Total Effect)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_n_proposals c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_number_proposals)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_n_proposals_lag  log_alexa_rank_lag log_forks_lag log_stars_lag lreddit_comments_lag log_Platform_Age_lag i.month, fe nest cnames(log_MC-Direct Effect) dec(2)  drop(i.month) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)


// n_topics with the similar number of control variables
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag log_Platform_Age_lag i.month, fe replace save(XTSCC_Mediation Effect_topic_7daylag) nest cnames(log_MC-Total Effect)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_N_topics  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_N_topics_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag  log_Platform_Age_lag i.month, fe nest cnames(log_N_topics)  drop(i.month) dec(3) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_N_topics_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag  log_Platform_Age_lag i.month, fe nest cnames(log_MC-Direct Effect) dec(2)  drop(i.month) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)

//Hashrate as mediator (old Baron and Kenny model)
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag  log_Platform_Age_lag i.month, fe replace save(XTSCC_Mediation_hashrate Effect) nest cnames(log_MC-Total Effect)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_hashrate  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag log_Platform_Age_lag log_hashrate_lag i.month, fe nest cnames(log_Hashrate)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_hashrate_lag log_alexa_rank_lag log_forks_lag log_stars_lag lreddit_comments_lag  log_Platform_Age_lag i.month, fe nest cnames(log_MC-Direct Effect) dec(2)  drop(i.month) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)

---------------------
//Adding the interaction term 

asdoc xtscc log_hashrate  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag c.log_Block_invHHI3_lag#c.log_Commit_invHHI_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag log_Platform_Age_lag log_hashrate_lag i.month, fe replace save(XTSCC_Interaction_effect) cnames(log_Hashrate)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_n_proposals c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag c.log_Block_invHHI3_lag#c.log_Commit_invHHI_lag log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_number_proposals)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_N_topics  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag c.log_Block_invHHI3_lag#c.log_Commit_invHHI_lag log_N_topics_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag  log_Platform_Age_lag i.month, fe nest cnames(log_N_topics)  drop(i.month) dec(3) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)

asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  c.log_Block_invHHI3_lag#c.log_Commit_invHHI_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  c.log_Block_invHHI3_lag#c.log_Commit_invHHI_lag   log_hashrate_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  c.log_Block_invHHI3_lag#c.log_Commit_invHHI_lag   log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
 asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  c.log_Block_invHHI3_lag#c.log_Commit_invHHI_lag   log_N_topics_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_MC)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)

 //volume as alternative measure
asdoc xtscc log_hashrate  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag log_Platform_Age_lag log_hashrate_lag i.month, fe replace save(XTSCC_Volume) cnames(log_Hashrate)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_n_proposals c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_number_proposals)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_N_topics  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_N_topics_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag  log_Platform_Age_lag i.month, fe nest cnames(log_N_topics)  drop(i.month) dec(3) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)

asdoc xtscc log_volume_USD c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag  c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_TotalVolume)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_volume_USD c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag   log_hashrate_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_TotalVolume)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_volume_USD c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_TotalVolume)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
 asdoc xtscc log_volume_USD c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_N_topics_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_TotalVolume)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)

 //total trading volume
asdoc xtscc log_total_volume c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag  c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_TotalVolume)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_total_volume c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag   log_hashrate_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_TotalVolume)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_total_volume c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_n_proposals_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_TotalVolume)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
 asdoc xtscc log_total_volume c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_N_topics_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag i.month, fe nest cnames(log_TotalVolume)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)


//Check main model with new sets of controls
log_MC log_social_attention_lag log_unique_authors_lag log_developer_attention_lag

asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag i.month, fe replace save(XTSCC_Mediation Effect-7d_lag) nest cnames(log_MC-Total Effect)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_n_proposals c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_n_proposals_lag log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag i.month, fe nest cnames(log_number_proposals)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_n_proposals_lag  log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag i.month, fe nest cnames(log_MC-Direct Effect) dec(2)  drop(i.month) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
//Second model with proposal as DV does not work with this set of controls, should it have the same set of controls as platform MC? 
xtscc log_n_proposals c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_n_proposals_lag log_forks_lag log_stars_lag log_unique_authors_lag log_Platform_Age_lag i.month, fe
//This set of controls would work for N_proposals, since these controls are more relevant to developmental related issues

// n_topics with the similar number of control variables
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag i.month, fe replace save(XTSCC_Mediation Effect_topic_7daylag) nest cnames(log_MC-Total Effect)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_N_topics  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag i.month, fe nest cnames(log_N_topics)  drop(i.month) dec(3) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_N_topics_lag  log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag i.month, fe nest cnames(log_MC-Direct Effect) dec(2)  drop(i.month) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)

//Same, middle model won't work, but below works
xtscc log_N_topics  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_forks_lag log_stars_lag log_unique_authors_lag log_Platform_Age_lag i.month, fe 
//hashrate
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag i.month, fe replace save(XTSCC_Mediation_hashrate Effect) nest cnames(log_MC-Total Effect)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_hashrate  c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag log_hashrate_lag i.month, fe nest cnames(log_Hashrate)  drop(i.month) dec(2) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
asdoc xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_hashrate_lag log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag i.month, fe nest cnames(log_MC-Direct Effect) dec(2)  drop(i.month) add(Platform Fixed Effect, YES, Month Fixed Effect, YES)
//hashrate does work except for the first model
xtscc log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag  log_forks_lag log_stars_lag log_unique_authors_lag log_Platform_Age_lag i.month, fe
//Suprisingly, the third model does work, but it's okay. It is full mediation

*After adding more controls, reduce the SEs,
xtivreg  log_MC log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag  log_social_attention log_public_interest log_unique_authors log_developer_attention log_hashrate_lag log_n_proposals_lag log_N_topics_lag  log_Platform_Age_lag (log_Block_invHHI3_lag log_Block_invHHI3_lag_sq log_Commit_invHHI_lag log_Commit_invHHI_lag_sq = mean_difficulty lmax_difficulty_lag lmax_difficulty_lag2_sq llCommit_invHHI_Top3_IV_lag llCommit_invHHI_Top10_IV_lag lCommit_invHHI_Top50per_IV_lag), fe vce(r) first small
//Best IV model sofar, CONSISTENT 
xtivreg  log_MC log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag  log_social_attention log_public_interest log_unique_authors log_developer_attention log_hashrate_lag log_n_proposals_lag log_N_topics_lag  log_Platform_Age_lag (log_Block_invHHI3_lag log_Block_invHHI3_lag_sq log_Commit_invHHI_lag log_Commit_invHHI_lag_sq = mean_difficulty lmean_difficulty_sq lmax_difficulty_lag lmax_difficulty_lag2_sq llCommit_invHHI_Top3_IV_lag llCommit_invHHI_Top10_IV_lag lCommit_invHHI_Top50per_IV_lag), fe vce(r) first small

//Most neat one with mediators, but no test statistics
xtivreg  log_MC log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_hashrate_lag log_n_proposals_lag log_N_topics_lag  log_Platform_Age_lag (log_Block_invHHI3_lag log_Block_invHHI3_lag_sq log_Commit_invHHI_lag log_Commit_invHHI_lag_sq = mean_difficulty lmean_difficulty_sq lmax_difficulty_lag lmax_difficulty_lag2_sq llCommit_invHHI_Top3_IV_lag llCommit_invHHI_Top10_IV_lag lCommit_invHHI_Top50per_IV_lag), fe vce(r) first small
 
//Most neat one without mediators
xtivreg  log_MC log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_Platform_Age_lag (log_Block_invHHI3_lag log_Block_invHHI3_lag_sq log_Commit_invHHI_lag log_Commit_invHHI_lag_sq = mean_difficulty lmean_difficulty_sq lmax_difficulty_lag lmax_difficulty_lag2_sq llCommit_invHHI_Top3_IV_lag llCommit_invHHI_Top10_IV_lag lCommit_invHHI_Top50per_IV_lag), fe vce(r) first small


//Suggested by the author
ivreg2  log_MC log_social_attention_lag log_unique_authors_lag log_developer_attention_lag platform_id log_Platform_Age_lag (log_Block_invHHI3_lag log_Block_invHHI3_lag_sq log_Commit_invHHI_lag log_Commit_invHHI_lag_sq = mean_difficulty lmean_difficulty_sq lmax_difficulty_lag lmax_difficulty_lag2_sq llCommit_invHHI_Top3_IV_lag llCommit_invHHI_Top10_IV_lag lCommit_invHHI_Top50per_IV_lag), r first small


//Now found new IV working for development decentraloization, but F statistics is still low for the operational 
xtivreg2 log_MC (x1 x2 x3 x4 = lmean_difficulty_lag lmax_difficulty_lag lmax_difficulty_lag_sq  lmax_difficulty_lag2 lmax_difficulty_lag2_sq log_mean_difficulty_lag2 log_mean_difficulty_lag2_sq post_rust post_hyperledger) log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag month, fe r first endog(x1 x2 x3 x4)

//This got the right significance but still weak iv and small sample
ivreghdfe log_MC (x1 x2 x3 x4 = lmax_difficulty_lag lmax_difficulty_lag_sq  lmax_difficulty_lag2 lmax_difficulty_lag2_sq  log_mean_difficulty_lag2 log_mean_difficulty_lag2_sq post_hyperledger) log_social_attention_lag log_unique_authors_lag log_developer_attention_lag log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag month, 2sls first cluster(platform_id) endog(x1 x2 x3 x4) partial(month)

//Best model so far but the mining decentralization are not significant (F passed Stock yogo requirement)
ivreghdfe log_MC (x1 x2 x3 x4 = log_mean_difficulty lmax_difficulty lmean_difficulty_lag lmean_difficulty_lag_sq  post_hyperledger ) log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag   log_Platform_Age_lag month, 2sls first dkraay(2) endog(x1 x2 x3 x4)

//This set of results have mining decentralization significant, but not the development decentralization

xtivreg2 log_MC (x1 x2 x3 x4 = log_mean_difficulty lmax_difficulty lmean_difficulty_lag  lmean_difficulty_sq post_hyperledger llCommit_invHHI_Top10_IV_lag) log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag log_Platform_Age_lag, first liml fe dkraay(3) endog(x1 x2 x3 x4)

xtivreg2 log_MC (x1 x2 x3 x4 = log_mean_difficulty lmax_difficulty lmean_difficulty_lag  lmean_difficulty_sq post_hyperledger llCommit_invHHI_Top10_IV_lag) log_alexa_rank_lag log_forks_lag log_stars_lag  lreddit_comments_lag log_Platform_Age_lag month, first fe dkraay(2) endog(x1 x2 x3 x4)


//step by step approaches - CONSISTENT
xtscc x1 log_mean_difficulty  log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_Platform_Age_lag reddit_subscribers lgithub_n_issues_lag month, fe
predict x1_hat,xb
xtscc x2 lmean_difficulty_sq log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_Platform_Age_lag reddit_subscribers lgithub_n_issues_lag month, fe
predict x2_hat
xtscc x3 lCommit_invHHI_Top5_IV lCommit_invHHI_Top50per_IV log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_Platform_Age_lag reddit_subscribers lgithub_n_issues_lag month, fe
predict x3_hat
xtscc x4 lCommit_invHHI_Top5_IV_sq  lCommit_invHHI_Top50per_IV_sq log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_Platform_Age_lag reddit_subscribers lgithub_n_issues_lag month, fe
predict x4_hat

//Second stage
xtscc log_MC c.x1_hat##c.x1_hat c.x3_hat##c.x3_hat log_alexa_rank_lag log_forks_lag log_stars_lag  log_reddit_comments_lag lreddit_posts_lag log_Platform_Age_lag reddit_subscribers lgithub_n_issues_lag month, fe
//overidentification
predict residuals, residuals
//Regress Residuals on Instruments: Regress the residuals on all the instruments and exogenous variables. This regression checks if the instruments are correlated with the residuals.
xtreg residuals log_mean_difficulty lmean_difficulty_sq Commit_invHHI_Top5_IV lCommit_invHHI_Top50per_IV lCommit_invHHI_Top5_IV_sq  lCommit_invHHI_Top50per_IV_sq  log_alexa_rank_lag log_forks_lag log_stars_lag log_reddit_comments_lag lreddit_posts_lag log_Platform_Age_lag reddit_subscribers lgithub_n_issues_lag month, fe
* Get the R-squared
display "Hansen J Statistic (Over-ID Test with DK SE): " e(N) * e(r2)

* Replace `df` with your degrees of freedom, 6 IV-4=2
display "Hansen J Test p-value: " chi2tail(3, 1.59571)


//under-identification test
ranktest (x1 x2 x3 x4) (log_mean_difficulty lmean_difficulty_sq  Commit_invHHI_Top5_IV lCommit_invHHI_Top50per_IV lCommit_invHHI_Top5_IV_sq  lCommit_invHHI_Top50per_IV_sq), robust
