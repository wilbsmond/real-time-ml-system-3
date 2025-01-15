# Session 4

## Goals 🎯

- [x] Show horizontal scaling in action
- [x] Add `candle_seconds` to our messages
- [x] Complete to-feature-store service
    - [x] Dockerize it

- [x] Docker compose file for our technical-indicators pipeline
- [ ] Start building the backfill pipeline.

## Questions

### Carlo Casorzo
*Should the technical indicators sdf first filter out the candles with different window size?*

YES!
*I was actually thinking that it would be a good idea to extend the candles service to produce all candles to the "candles" topic with base key, ex: "BTCUSD", but maybe also to a filtered one for its own window size with a separate key, ex: "key:BTCUSD-1m"*

### Stefan Pajovic
First partition ih handling 2 keys, so 4th partition is obsolete. So this means we can implement new partition obefore we introduce new keys, then new key is going to new partition? Do I get this right? :)

### Jayant Sharma
will the combination of pair and candle_seconds ensure a unique primary key everytime?

### Ichun yeh
do we need to add `depends_on` in `technical-indicators-pipeline.yml`? or not because these are not strong dependencies?