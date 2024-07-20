#!/bin/bash -e

log="/tmp/vpu-test.log"
h264="h264_w1920_h1080_f25_r4_p1_8bit_54f_11mb_high_cabac.264"
decode_yuv="/tmp/decode.yuv"
decode_md5="e59c9318e3f733d016ebfcdec98a95fb"
yuv="yuv420p_w1280_h720_30f.yuv"
encode_264="/tmp/encode.264"
encode_md5="55ceae7750bdc3906dd427e221c0317b"

while true
do
    rm -f $log

    # decode routine
    echo "`date`" >> $log
    rm -f $decode_yuv
    mvx_decoder -f raw /opt/factorytest/res/h264_w1920_h1080_f25_r4_p1_8bit_54f_11mb_high_cabac.264 $decode_yuv >> $log
    [ -f $decode_yuv ] || exit -1
    md5=`md5sum $decode_yuv | awk '{ print $1 }'`
    [ "$md5" == "$decode_md5" ] || exit -1

    # encode routine
    echo "`date`" >> $log
    rm -f $encode_264
    mvx_encoder -f raw -w 1280 -h 720 /opt/factorytest/res/yuv420p_w1280_h720_30f.yuv $encode_264 >> $log
    [ -f $encode_264 ] || exit -1
    md5=`md5sum $encode_264 | awk '{ print $1 }'`
    [ "$md5" == "$encode_md5" ] || exit -1
done