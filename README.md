# 프로젝트 소개
<p align="center">
  <img src="https://github.com/addinedu-amr-2th/robo-reop-3/assets/117617384/a47b33db-8e67-4869-9070-062e9dd757f5">
</p>
로봇의 카메라를 와 OpenCV를 이용하여 모터를 제어하는 프로젝트

# 시연 영상
<p align="center">
  <img src="https://github.com/addinedu-amr-2th/robo-reop-3/assets/117617384/1d556166-901f-4862-bec8-a2010ec72a7f">
</p>

# 목적
-실제 도로와 비슷한 주행로 환경을 구현하여 로봇의 이미지 만을 가지고 차선의 중앙을 찾아내서 주행해보자



-딥 러닝 모델을 사용하지 않은 상태로 차선을 인식하여 주행

# 프로젝트 설명

* 이미지 전처리
<p align="center">
  <img src="https://github.com/addinedu-amr-2th/robo-reop-3/assets/124948850/c98020c5-f978-4144-9251-24264e1bfd1f">
</p>

* opencv를 이용하여 도로 이미지 가공<br/>
  <br/> 1.카메라를 통해 본 이미지
  <br/> 2.ROI(Region of Interest)를 설정해 원하는 대상만 남김
  <br/> 3.HLS 필터를 이용하여 원하는 색범위안의 물체만 인식
  <br/> 4.Gray scale과 thershold를 통해 binarization
  <br/> 5.perspective Transform를 통해 양쪽의 차선을 일직선으로 배치
  <br/> 6.sliding_window 곡선을 곡선으로 인식하기위해 사용


  
* 전체 시스템 구성도<br/>
<p align="center">
<img src="https://github.com/addinedu-amr-2th/robo-reop-3/assets/124948850/016970c8-fd77-4205-a0d0-ddf4d85bfed7">
</p>
<p align="center">
<img src="https://github.com/addinedu-amr-2th/robo-reop-3/assets/124948850/ce566f23-ede3-44e7-901d-7dae5ae936ad">
</p>

  * 이미지 전처리후 아래 2번 사진의 두개의 선의 픽셀 차이값을 가지고 로봇의 모터를 제어
  <br/>  1번 사진 왼쪽 차선과 오른쪽 차선의 인식양을 인식하다가 표준값 보다 픽셀양이 적다면 한쪽으로 치우쳐져 있다고 판단
  <br/>  3번 사진은 교차로를 만나을때의 사진인데 사진 상단의 양쪽 픽셀 값이 없어진다면 직진을 하도록 제어
  


# 의의
- 주행중에 차선의 중앙을 인식하여 차선에서 벗어나는것을 방지하기 위해서는 최소한의 딜레이와 가벼운 코드가 필요하다.
  <br/> 그럴때 우리의 코드는 훌륭한 해결 방안중에 1안이 될거라고 믿습니다.
  <br/> 딥러닝 모델을 활용하여 인식하는 것이 아닌 Open CV를 사용하여 가볍고 빠른 인식이 가능할 것이하고 판단된다.

#  회고
- 하드 웨어의 한계
  - 로봇에 기본적으로 탑제 되었던 라즈베리 카메라의 경우 카메라의 이미지가 필요했던 이미지 보다 시야각이 너무 좁게 나와서 카메라의 이미지와 코드의 호환이 불가능하여 하드웨어의 구조 변경 및 외부 카메라(lenovo 웹캡)를 추가로 장착하여 진행하였다.
- 계획대로 흘러가지 않는 개발 상황
  - 원초의 목표는 크게 잡았지만 처음 잡아 놓은목표중 가장 베이스에서 프로젝트를 마감하게 되었다.<br/> 하드웨어적 문제나 팀과의 소통 미스로 인한것들 등이 원인이라 파악된다.<br/>이를 통하여 팀과의 회의를통하여 정보 공유 및 목표치의 변경에 유하게 진행하는 방법을 알게 되었다.
# 코드 정리
- /lane_distance : 차선의 중앙 값과 이미지의 중앙값의 차이값을 모터 제어를 위해 송출할때 사용하는 토픽
- /right_distance_difference : 오른쪽 차선의 인식된 픽셀 값을 송출할때 사용하는 토픽
- /left_distance_difference : 왼쪽 차선의 인식된 픽셀 값을 송출할때 사용하는 토픽
- /intersection_flag : 교차로를 인식하였을때 특정 값을 송출할때 사용하는 토픽
- controll_node : 위 토픽을 발행하기 위한 노드
- cmd_vel : Twist 형식의 직접적으로 모터를 제어하기 위해 발행하는 토픽
- teleop_twist_publisher : cmd_vel을 발행하기 위한 노드(linear.x, angular.z 이 두개를 위주로 제어한다.)
# 발표 자료
[발표 PPT][link_ppt]

[link_ppt]: https://docs.google.com/presentation/d/1TdLDWyX7o4_dsa_KVFDCJpya4sgQwAyP/edit?usp=drive_link&ouid=114791632627429619927&rtpof=true&sd=true "PPT_link"
# 팀원 소개
[신대준][link_1]<br/>
[김세연][link_2]<br/>
[이용욱][link_3]<br/>

[link_1]: https://github.com/addinedu-amr-2th/robo-reop-3 "GitHub_link"
[link_2]: https://github.com/addinedu-amr-2th/robo-reop-3 "GitHub_link"
[link_3]: https://github.com/addinedu-amr-2th/robo-reop-3 "GitHub_link"
