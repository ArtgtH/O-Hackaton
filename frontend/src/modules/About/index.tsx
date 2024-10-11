import pc from "@/assets/computer.jpg";
import Typography from "@/ui/Typography.tsx";

export const About = () => {
  return (
    <div className="w-full h-full flex flex-col gap-24 justify-start items-center">
      <div className="flex flex-col gap-10 max-w-[1000px] mt-20">
        <Typography variant="h1" className="flex gap-2 text-lime-300">
          Fullstack Excel
        </Typography>
        <Typography
          variant="h4"
          className="flex gap-2 text-yellow-500 font-semibold"
        >
          КЕЙС - РАЗРАБОТКА МОДЕЛИ ДЛЯ ТЭГИРОВАНИЯ ТАРИФОВ
        </Typography>
        <Typography
          variant="h6"
          className="flex gap-2 text-white font-semibold"
        >
          Наше решение основано на ⚡️⚡️⚡️ blazingly fast ⚡️⚡️⚡️ языковых
          моделях, которые запускаются с помощью ONNX. Для обучения моделей были
          использованы такие SOTA решения как Tf-Idf и ЛогРегрессия, а так же
          трижды дистилированный 🥃🥃🥃 и квантизованный ⚛⚛⚛ mini-BERT. Мы не
          ограничились одной лишь моделью - мы написали backend на go для
          демонстрации взаимодействия с моделью и интеграции модели в ваши
          сервисы.
        </Typography>
      </div>
      <div className="flex flex-col gap-10 max-w-[1000px] w-full">
        <Typography variant="h1" className="flex gap-2 text-lime-300">
          Команда
        </Typography>
        <Typography
          variant="h4"
          className="flex gap-2 text-yellow-500 font-semibold"
        >
          СПБГУ, ИТМО
        </Typography>
        <div className="flex gap-10 flex-wrap">
          <Typography
            variant="h6"
            className="flex gap-2 text-white font-semibold"
          >
            Максим Игитов - ТИМЛИД
          </Typography>
          <Typography
            variant="h6"
            className="flex gap-2 text-white font-semibold"
          >
            Всеволод Богодист - МЛ/ДЛ
          </Typography>
          <Typography
            variant="h6"
            className="flex gap-2 text-white font-semibold"
          >
            Георгий Грушевский - МЛ/ДЛ
          </Typography>
          <Typography
            variant="h6"
            className="flex gap-2 text-white font-semibold"
          >
            Андрей Горошко - ФРОНТЕНД
          </Typography>
          <Typography
            variant="h6"
            className="flex gap-2 text-white font-semibold"
          >
            Артём Вичук - БЭКЕНД
          </Typography>
        </div>
      </div>
      <img src={pc} alt="" className="rounded-xl mt-12 mb-40" />
    </div>
  );
};
