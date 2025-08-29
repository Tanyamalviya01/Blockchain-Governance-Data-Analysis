* Blockchain Governance Analysis
clear all
set more off

* Load the cleaned dataset
import delimited "../all_11platforms_STATA_READY.csv", clear

* Drop ALL potentially existing variables
capture drop platform_id
capture drop time_var
capture drop date
capture drop log_*
capture drop month
capture drop lreddit_*
capture drop lgithub_n_issues

* Create platform ID and time variable
encode platform, gen(platform_id)
gen time_var = year * 100 + week

* Convert to proper date format
gen date = weekly(string(year) + "w" + string(week), "YW")
format date %tw
xtset platform_id date

* Generate log transformations
gen log_MC = ln(market_cap) if market_cap > 0 & market_cap != .
gen log_Block_invHHI3 = ln(block_hhi) if block_hhi > 0 & block_hhi != .
gen log_Commit_invHHI = ln(commit_hhi) if commit_hhi > 0 & commit_hhi != .
gen log_hashrate = ln(hashrate) if hashrate > 0 & hashrate != .
gen log_volume_USD = ln(volume_usd) if volume_usd > 0 & volume_usd != .

* Handle proposal variables (check if they exist) - FIXED SYNTAX
capture confirm variable number_proposal
if _rc == 0 {
    gen log_n_proposals = ln(number_proposal + 1) if number_proposal >= 0 & number_proposal != .
}
if _rc != 0 {
    gen log_n_proposals = .
    display "Warning: number_proposal variable not found"
}

capture confirm variable topic_diversity
if _rc == 0 {
    gen log_N_topics = ln(topic_diversity + 1) if topic_diversity >= 0 & topic_diversity != .
}
if _rc != 0 {
    gen log_N_topics = .
    display "Warning: topic_diversity variable not found"
}

* Generate control variables (with existence checks) - FIXED SYNTAX
capture confirm variable forks
if _rc == 0 {
    gen log_forks = ln(forks) if forks > 0 & forks != .
}
if _rc != 0 {
    gen log_forks = .
    display "Warning: forks variable not found"
}

capture confirm variable stars
if _rc == 0 {
    gen log_stars = ln(stars) if stars > 0 & stars != .
}
if _rc != 0 {
    gen log_stars = .
    display "Warning: stars variable not found"
}

* Reddit variables with robust checking - FIXED SYNTAX
capture confirm variable reddit_comments
if _rc == 0 {
    gen log_reddit_comments = ln(reddit_comments + 1) if reddit_comments >= 0 & reddit_comments != .
}
if _rc != 0 {
    gen log_reddit_comments = .
    display "Warning: reddit_comments variable not found"
}

capture confirm variable reddit_posts
if _rc == 0 {
    gen lreddit_posts = ln(reddit_posts + 1) if reddit_posts >= 0 & reddit_posts != .
}
if _rc != 0 {
    gen lreddit_posts = .
    display "Warning: reddit_posts variable not found"
}

* Handle reddit_subscribers with multiple attempts - FIXED SYNTAX
gen log_reddit_subscribers = .
gen reddit_subscribers_copy = .

capture confirm variable reddit_subscribers
if _rc == 0 {
    replace log_reddit_subscribers = ln(reddit_subscribers) if reddit_subscribers > 0 & reddit_subscribers != .
    replace reddit_subscribers_copy = reddit_subscribers
}
if _rc != 0 {
    capture confirm variable Reddit_Subscribers
    if _rc == 0 {
        replace log_reddit_subscribers = ln(Reddit_Subscribers) if Reddit_Subscribers > 0 & Reddit_Subscribers != .
        replace reddit_subscribers_copy = Reddit_Subscribers
    }
    if _rc != 0 {
        display "Warning: reddit_subscribers variable not found"
    }
}

* Platform age variable - FIXED SYNTAX
capture confirm variable platform_age
if _rc == 0 {
    gen log_Platform_Age = ln(platform_age) if platform_age > 0 & platform_age != .
}
if _rc != 0 {
    capture confirm variable Platform_age
    if _rc == 0 {
        gen log_Platform_Age = ln(Platform_age) if Platform_age > 0 & Platform_age != .
    }
    if _rc != 0 {
        gen log_Platform_Age = .
        display "Warning: platform_age variable not found"
    }
}

* Create placeholder variables for missing data
gen log_alexa_rank = .
gen lgithub_n_issues = .

* Generate lagged variables
gen log_Block_invHHI3_lag = L.log_Block_invHHI3
gen log_Commit_invHHI_lag = L.log_Commit_invHHI
gen log_hashrate_lag = L.log_hashrate
gen log_n_proposals_lag = L.log_n_proposals
gen log_N_topics_lag = L.log_N_topics
gen log_forks_lag = L.log_forks
gen log_stars_lag = L.log_stars
gen lreddit_comments_lag = L.log_reddit_comments
gen lreddit_posts_lag = L.lreddit_posts
gen log_reddit_subscribers_lag = L.log_reddit_subscribers
gen log_Platform_Age_lag = L.log_Platform_Age

* Generate month variable
gen month = month(dofC(date))

* Display variable availability summary
display "=== VARIABLE AVAILABILITY SUMMARY ==="
count if !missing(log_MC)
display "log_MC available: " r(N) " observations"

count if !missing(log_Block_invHHI3_lag)
display "log_Block_invHHI3_lag available: " r(N) " observations"

count if !missing(log_Commit_invHHI_lag)
display "log_Commit_invHHI_lag available: " r(N) " observations"

count if !missing(log_hashrate_lag)
display "log_hashrate_lag available: " r(N) " observations"

* Check data availability for core analysis
count if !missing(log_MC, log_Block_invHHI3_lag, log_Commit_invHHI_lag)
local complete_obs = r(N)
display "Observations with complete core data: " `complete_obs'

if `complete_obs' > 50 {
    
    display "=== RUNNING ANALYSIS WITH AVAILABLE DATA ==="
    
    * Model 1: Basic Market Cap model
    display "Running Model 1: Basic Market Cap Analysis..."
    xtreg log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag i.month, fe robust
    estimates store mc_basic_model
    
    * Model 2: Market Cap with available controls
    count if !missing(log_MC, log_Block_invHHI3_lag, log_Commit_invHHI_lag, log_forks_lag, log_stars_lag)
    if r(N) > 30 {
        display "Running Model 2: Market Cap with GitHub Controls..."
        xtreg log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_forks_lag log_stars_lag i.month, fe robust
        estimates store mc_controls_model
    }
    
    * Model 3: Hashrate mediation
    count if !missing(log_hashrate, log_Block_invHHI3_lag, log_Commit_invHHI_lag)
    if r(N) > 30 {
        display "Running Model 3: Hashrate Analysis..."
        xtreg log_hashrate c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag i.month, fe robust
        estimates store hashrate_model
        
        * Market cap with hashrate mediation
        count if !missing(log_MC, log_Block_invHHI3_lag, log_Commit_invHHI_lag, log_hashrate_lag)
        if r(N) > 30 {
            display "Running Model 4: Market Cap with Hashrate Mediation..."
            xtreg log_MC c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag log_hashrate_lag i.month, fe robust
            estimates store mc_hashrate_model
        }
    }
    
    * Model 5: Volume as alternative outcome
    count if !missing(log_volume_USD, log_Block_invHHI3_lag, log_Commit_invHHI_lag)
    if r(N) > 30 {
        display "Running Model 5: Volume Analysis..."
        xtreg log_volume_USD c.log_Block_invHHI3_lag##c.log_Block_invHHI3_lag c.log_Commit_invHHI_lag##c.log_Commit_invHHI_lag i.month, fe robust
        estimates store volume_model
    }
    
    * Display comprehensive results
    display "=== COMPREHENSIVE RESULTS TABLE ==="
    estimates table mc_basic_model mc_controls_model hashrate_model mc_hashrate_model volume_model, ///
        stats(N r2_w) star(0.1 0.05 0.01) b(%7.4f) t(%7.2f)
    
    * Save all estimates
    estimates save final_corrected_analysis, replace
    
    display "=== ANALYSIS COMPLETED SUCCESSFULLY ==="
    display "Methodology implemented:"
    display "- Square terms via c.var##c.var specification"
    display "- Lagged independent variables as requested"
    display "- Platform and month fixed effects"
    display "- Robust standard errors"
    display "- Complete mediation analysis structure"
    
}
if `complete_obs' <= 50 {
    display "ERROR: Insufficient observations with complete core data (" `complete_obs' ")"
    display "Need at least 50 observations for meaningful analysis"
}
