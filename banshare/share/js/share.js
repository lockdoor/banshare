function shareGenre(shareGenre){
    var description;
    var arr = [' เท้าแชร์ยกหัว ', ' เท้าแชร์หักค้ำท้าย ', ' รับตามมือจอง ', ' บิท ']
    for (letter in shareGenre){
        if (letter == '1'){
            description += arr[letter];
        }
    }
    return description;
}