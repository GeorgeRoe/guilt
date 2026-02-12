export const EYE_OPEN = `                         ...',;;:cccccccc:;,..
                     ..,;:cccc::::ccccclloooolc;'.
                  .',;:::;;;;:loodxk0kkxxkxxdocccc;;'..
                .,;;;,,;:coxldKNWWWMMMMWNNWWNNKkdolcccc:,.
             .',;;,',;lxo:...dXWMMMMMMMMNkloOXNNNX0koc:coo;.
          ..,;:;,,,:ldl'   .kWMMMWXXNWMMMMXd..':d0XWWN0d:;lkd,
        ..,;;,,'':loc.     lKMMMNl. .c0KNWNK:  ..';lx00X0l,cxo,.
      ..''....'cooc.       c0NMMX;   .l0XWN0;       ,ddx00occl:.
    ..'..  .':odc.         .x0KKKkolcld000xc.       .cxxxkkdl:,..
  ..''..   ;dxolc;'         .lxx000kkxx00kc.      .;looolllol:'..
 ..'..    .':lloolc:,..       'lxkkkkk0kd,   ..':clc:::;,,;:;,'..
 ......   ....',;;;:ccc::;;,''',:loddol:,,;:clllolc:;;,'........
     .     ....'''',,,;;:cccccclllloooollllccc:c:::;,'..
             .......'',,,,,,,,;;::::ccccc::::;;;,,''...
               ...............''',,,;;;,,''''''......
                    ............................`

export const EYE_HALFWAY = `                         ...'',;;;;::;;;,'..
                     ..,;:cloodddxxxkkkkkkkkxol;..
                  .';codxxkkk000000000000kkkkkkxdoc,..
                .,codxk0000000000000000000000000kkxddoc,..
             .':ldxk00000000000000000000000000000000kkxxol:'
          .,:ldxkk000000000K000000000000000K0000000000kkxkkx:.
       ..,coxkk000000000000000kk000000000000000000000000kxxxxl'
      .,;codxxkk00000000kkk0KK0XNWWWWWWWWWNX0kkkkk00000kkxdool;.
    .';::ccldk00KKKK00oc;..,x00KNNXXXXXNNX0000000000kkkkkkxoc:,..
  ..,;,'..,o00000kkxo,       ,lkKKKKKK0K0d,.;ldk000KK0kxxxdoc:'..
 ..,,'.  .,lk0xxxdol:,..       .,ldddl:,.   .,codkk00kxdollc:,...
 ..'.......',;:c::cclccc::;,,,',,;::::;,;;:clodddxdol:;::;'......
    .....  ...''',,,;;;:ccllloooooooooooooolllcccc:;;,....
             .......'',,,,,,;;;:::ccclllccc:::;;;,''...
               ..............'''',,;;;;;,,,''''......
                    .............................`

export const EYE_SHUT = `                         ...'',;;;;;;;,,...
                    ..,:loxkk000000KKKKKK00xdc,..
                 .,cox000KXXXXXXXXXXXXXXXXXXXK00xo:,..
              ..;lx000KKKKK000000000000000KKKKXXXXK00xl;..
           ..,:oxk00000000000000000000000000000000KKKKKK0d:.
        ..;codxkk000kkkkkkkxxxxxxxxxxxxxxxxkkkkkk000000KK0kl'
      ..;ldxkkkkkkxxxxxddddddddddddddddddddddddxxxxxxkkk000xc.
    ..,:oxxkkkkkxxxxdddddddddddddddddddddddddddddddddxxkkkkxl;.
  ..,;codxxkkkxxddddddddddddddddddddddddddddddddxdxxxk000kxdo:..
 .';::::cldk000kkkxxxxxxdddddddddddddddddddddxxxxxkk0000xkddl;..
.';:;,..,ckXXXKKK0KK000kxk0doddxxdddddddxxxxxxkk0000kkkkkxdoc,..
.',,''..,:oxxxxxxxkkxkkxk00xxk000000000000KKKKKKK000kxdllll:,..
 .........',,,:ccllllooooxkxxx000kk0000000000000000kxdoc,'...
         ......',;;::cc::clllloddoox0xdxxkxxxxddollllc:'.
              .....'',,,,,,,;;;;;::cllc::ccc::;;,,,'...
               ..................'''..'''......`

const BLINK_DURATION = 450
const BLINK_CHANCE = 0.25

export function useAsciiEye() {
  const eyeAsciiArt = ref(EYE_OPEN)

  function blink() {
    eyeAsciiArt.value = EYE_HALFWAY
    setTimeout(() => {
      eyeAsciiArt.value = EYE_SHUT
      setTimeout(() => {
        eyeAsciiArt.value = EYE_HALFWAY
        setTimeout(() => {
          eyeAsciiArt.value = EYE_OPEN
        }, BLINK_DURATION / 4)
      }, BLINK_DURATION / 2)
    }, BLINK_DURATION / 4)
  }

  onMounted(() => {
    setInterval(() => {
      if (Math.random() < BLINK_CHANCE) blink()
    }, BLINK_DURATION * 4)
  })

  return readonly(eyeAsciiArt)
}