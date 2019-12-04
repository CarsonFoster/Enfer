<?xml version="1.0" encoding="UTF-8"?>
<tileset name="Tiles" tilewidth="16" tileheight="16" tilecount="100" columns="10">
 <image source="tiles.png" width="160" height="160"/>
 <terraintypes>
  <terrain name="Volcano" tile="21"/>
 </terraintypes>
 <tile id="0">
  <properties>
   <property name="Type" value="Kill"/>
  </properties>
  <objectgroup draworder="index">
   <object id="1" name="SpikeCollision" x="2.30435" y="15.5652">
    <polygon points="0,0 0.956522,-4.08696 2.30435,-7.17391 3.13043,-9.08696 4.26087,-10.1739 5.04348,-11.0435 8.17391,-11.3043 8.26087,-8.13043 9.21739,-7.13043 9.13043,-5.04348 10.2174,-4.21739 10.3478,-2.17391 11.3913,-2.21739 11.3043,0"/>
   </object>
  </objectgroup>
 </tile>
 <tile id="10" terrain=",,,0">
  <properties>
   <property name="Type" value="Walkable&amp;Climbable"/>
  </properties>
 </tile>
 <tile id="11" terrain=",,0,0">
  <properties>
   <property name="Type" value="Walkable"/>
  </properties>
 </tile>
 <tile id="12" terrain=",,0,">
  <properties>
   <property name="Type" value="Walkable&amp;Climbable"/>
  </properties>
 </tile>
 <tile id="14" terrain=",,,0">
  <properties>
   <property name="Type" value="Walkable&amp;Climbable"/>
  </properties>
 </tile>
 <tile id="15" terrain=",,0,">
  <properties>
   <property name="Type" value="Walkable&amp;Climbable"/>
  </properties>
 </tile>
 <tile id="16">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="17">
  <properties>
   <property name="Type" value="Kill"/>
  </properties>
 </tile>
 <tile id="18">
  <properties>
   <property name="Type" value="SolidNoOther"/>
  </properties>
 </tile>
 <tile id="19">
  <properties>
   <property name="Type" value="Walkable"/>
  </properties>
 </tile>
 <tile id="20" terrain=",0,,0">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="21" terrain="0,0,0,0">
  <properties>
   <property name="Type" value="SolidNoOther"/>
  </properties>
 </tile>
 <tile id="22" terrain="0,,0,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="24" terrain=",0,,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="25" terrain="0,,,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="26">
  <properties>
   <property name="Type" value="Walkable&amp;Climbable"/>
  </properties>
 </tile>
 <tile id="28">
  <properties>
   <property name="Type" value="Sign"/>
  </properties>
 </tile>
 <tile id="30" terrain=",0,,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="31" terrain="0,0,,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="32" terrain="0,,,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="37" terrain=",0,,0">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="38" terrain="0,,0,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="46" terrain=",,0,0">
  <properties>
   <property name="Type" value="Walkable"/>
  </properties>
 </tile>
 <tile id="47" terrain=",0,0,0">
  <properties>
   <property name="Type" value="SolidNoOther"/>
  </properties>
 </tile>
 <tile id="48" terrain="0,,0,0">
  <properties>
   <property name="Type" value="SolidNoOther"/>
  </properties>
 </tile>
 <tile id="49" terrain=",,0,0">
  <properties>
   <property name="Type" value="Walkable"/>
  </properties>
 </tile>
 <tile id="56" terrain="0,0,,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="57" terrain="0,0,,0">
  <properties>
   <property name="Type" value="SolidNoOther"/>
  </properties>
 </tile>
 <tile id="58" terrain="0,0,0,">
  <properties>
   <property name="Type" value="SolidNoOther"/>
  </properties>
 </tile>
 <tile id="59" terrain="0,0,,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="60">
  <properties>
   <property name="Type" value="Walkable"/>
  </properties>
 </tile>
 <tile id="61">
  <properties>
   <property name="Type" value="Walkable"/>
  </properties>
 </tile>
 <tile id="62">
  <properties>
   <property name="Type" value="Walkable"/>
  </properties>
 </tile>
 <tile id="64">
  <properties>
   <property name="Type" value="Kill"/>
  </properties>
  <objectgroup draworder="index">
   <object id="2" name="LavaCollision" x="-0.0434783" y="9.04348">
    <polygon points="0,0 0.0434783,6.95652 16.0435,6.91304 16.0435,-0.0434783"/>
   </object>
  </objectgroup>
  <animation>
   <frame tileid="64" duration="200"/>
   <frame tileid="74" duration="200"/>
   <frame tileid="84" duration="200"/>
   <frame tileid="94" duration="200"/>
  </animation>
 </tile>
 <tile id="67" terrain=",0,,0">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
 <tile id="68" terrain="0,,0,">
  <properties>
   <property name="Type" value="Climbable"/>
  </properties>
 </tile>
</tileset>
