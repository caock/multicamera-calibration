#conda activate multicamera-calibration

frame_name='frame_3'

# python3 ./scripts/video2img.py -i ./calibration/IMG_0714.MOV -o ./calibration/IMG_0714/
# python3 ./scripts/video2img.py -i ./calibration/IMG_0715.MOV -o ./calibration/IMG_0715/
# python3 ./scripts/rotate_images.py ./calibration/AcquisitionMultipleThread/camera_19238308/\*.png
# python3 ./scripts/rotate_images.py ./calibration/AcquisitionMultipleThread/camera_19371018/\*.png

cd build && make && cd .. 
#python3 ./build/bin/intrinsic  ./calibration/AcquisitionMultipleThread/camera_19238308/\*.png ./calibration/output/intrinsic_camera_19238308.json -p 'chessboard' -n 9 -W 9 -H 6
#python3 ./build/bin/intrinsic  ./calibration/AcquisitionMultipleThread/camera_19346452/\*.png ./calibration/output/intrinsic_camera_19346452.json -p 'chessboard' -n 9 -W 9 -H 6
#python3 ./build/bin/intrinsic  ./calibration/AcquisitionMultipleThread/camera_19371018/\*.png ./calibration/output/intrinsic_camera_19371018.json -p 'chessboard' -n 9 -W 9 -H 6
#python3 ./build/bin/intrinsic  ./calibration/AcquisitionMultipleThread/camera_19405866/\*.png ./calibration/output/intrinsic_camera_19405866.json -p 'chessboard' -n 9 -W 9 -H 6

python3 ./build/bin/extrinsic ./calibration/output/intrinsic_camera_19238308.json ./calibration/AcquisitionMultipleThread/camera_19238308/${frame_name}.png ./calibration/output/extrinsic_camera_19238308.json  -p True
python3 ./build/bin/extrinsic ./calibration/output/intrinsic_camera_19346452.json ./calibration/AcquisitionMultipleThread/camera_19346452/${frame_name}.png ./calibration/output/extrinsic_camera_19346452.json -p True
python3 ./build/bin/extrinsic ./calibration/output/intrinsic_camera_19371018.json ./calibration/AcquisitionMultipleThread/camera_19371018/${frame_name}.png ./calibration/output/extrinsic_camera_19371018.json -p True
python3 ./build/bin/extrinsic ./calibration/output/intrinsic_camera_19405866.json ./calibration/AcquisitionMultipleThread/camera_19405866/${frame_name}.png ./calibration/output/extrinsic_camera_19405866.json -p True


#cd build && make && cd .. && python3 ./build/bin/check_3d ./calibration/output/intrinsic_{}.json ./calibration/output/extrinsic_{}.json ./calibration/AcquisitionMultipleThread/{}/${frame_name}.png  camera_19238308,camera_19346452,camera_19371018,camera_19405866

#python3 ./build/bin/build_ba -f /home/user1/{}/points.json ./calibration/output/intrinsic_{}.json ./calibration/output/extrinsic_{}.json /home/user1/{}/annotations/\*.pos /home/user1/ba_problem.txt camera_19238308,camera_19346452,camera_19371018,camera_19405866
